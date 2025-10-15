# Recipes API Service - Refactoring Plan

## Executive Summary

This document outlines a prioritized refactoring plan to address architectural issues, code quality concerns, and technical debt in the recipes-api-service. The plan is organized by priority (P0-P3) and includes estimated effort, risk assessment, and implementation order.

---

## Priority Levels

- **P0 (Critical)**: Security, correctness, or data integrity issues - must fix immediately
- **P1 (High)**: Performance issues, significant code quality problems affecting maintainability
- **P2 (Medium)**: Technical debt, code organization, developer experience improvements
- **P3 (Low)**: Nice-to-have improvements, documentation enhancements

---

## Phase 1: Critical Fixes (P0) - Weeks 1-2

### 1.1 Fix Broad Exception Catching
**Priority**: P0
**Effort**: 1 week
**Risk**: High - Could expose hidden bugs
**Files**: `src/services/recipe.py`, `src/services/recipe_slot_assignment.py`

**Problem**:
- Catching generic `Exception` masks bugs and makes debugging difficult
- Silent failures in slot assignment loop

**Solution**:
```python
# Before
try:
    result = some_operation()
except Exception as e:
    logger.error("Something went wrong")
    raise ServerError("Generic error")

# After
try:
    result = some_operation()
except SpecificError as e:
    logger.error(f"Specific operation failed: {e}", exc_info=True)
    raise
except AnotherSpecificError as e:
    logger.error(f"Another operation failed: {e}", exc_info=True)
    raise KnownAPIError("User-friendly message") from e
```

**Implementation Steps**:
1. Identify all `except Exception` blocks
2. Determine specific exceptions that should be caught
3. Add proper exception hierarchy if needed
4. Update error handling to be more granular
5. Add tests for each error path

**Success Metrics**:
- Zero generic exception catches remaining
- All error paths have specific exception types
- Error messages include context for debugging

---

### 1.2 Fix Cycle Date Validation Logic
**Priority**: P0
**Effort**: 3 days
**Risk**: Medium - Business logic change
**Files**: `src/services/recipe.py`

**Problem**:
- Validation logic duplicated across `create_recipe`, `update_recipe`, `delete_recipe`
- Cutoff window logic scattered and hard to maintain
- Inconsistent error messages

**Solution**:
Create a dedicated validation module:

```python
# src/validators/cycle_date_validator.py
from datetime import datetime, timedelta
from typing import Tuple

class CycleDateValidator:
    """Centralized cycle date validation logic"""

    def __init__(self, partner_repo):
        self._partner_repo = partner_repo

    def validate_cycle_date(
        self,
        cycle_date: datetime,
        partner_id: str,
        operation: str  # 'create', 'update', 'delete'
    ) -> Tuple[bool, str]:
        """
        Validate cycle date for recipe operations.

        Returns: (is_valid, error_message)
        """
        # 1. Check if Monday
        if cycle_date.weekday() != 0:
            return False, "Cycle date must be a Monday"

        # 2. Check if future date
        if cycle_date < datetime.now():
            return False, "Cycle date must be in the future"

        # 3. Check cutoff window
        cutoff_days = self._partner_repo.get_cutoff_days(partner_id)
        cutoff_date = datetime.now() + timedelta(days=cutoff_days)

        if cycle_date < cutoff_date:
            return False, f"Cycle date is within {operation} cutoff window ({cutoff_days} days)"

        return True, ""
```

**Implementation Steps**:
1. Create `src/validators/` directory
2. Implement `CycleDateValidator` class
3. Add comprehensive unit tests
4. Refactor `RecipeService` to use validator
5. Update error handling to use consistent messages

---

## Phase 2: High Priority Improvements (P1) - Weeks 3-5

### 2.1 Address N+1 Query Problem
**Priority**: P1
**Effort**: 2 weeks
**Risk**: Medium - Performance testing required
**Files**: `src/services/recipe.py`, `src/db/recipes_repo.py`

**Problem**:
- `get_all_recipes` and other methods fetch data in loops
- Multiple round trips to database and external services
- Poor performance with large datasets

**Solution**:
```python
# Before
def get_all_recipes(self, partner_id: str) -> list[RecipeResponse]:
    recipe_refs = self._recipes_repo.get_all_recipe_refs_by_partner(partner_id)
    recipes = []
    for ref in recipe_refs:  # N+1 problem
        recipe = self._culops_client.get_recipe(ref.culops_recipe_id)
        recipes.append(recipe)
    return recipes

# After
def get_all_recipes(self, partner_id: str) -> list[RecipeResponse]:
    recipe_refs = self._recipes_repo.get_all_recipe_refs_by_partner(partner_id)
    recipe_ids = [ref.culops_recipe_id for ref in recipe_refs]

    # Batch fetch
    recipes = self._culops_client.get_recipes_batch(recipe_ids)

    return recipes
```

**Implementation Steps**:
1. Audit all methods for N+1 patterns
2. Add batch operations to repositories
3. Update clients to support batch fetching
4. Add performance benchmarks
5. Optimize database queries with JOINs where appropriate

**Success Metrics**:
- 50%+ reduction in database queries for list operations
- Response time improvement measured and documented

---

### 2.2 Refactor Partner-Specific Logic
**Priority**: P1
**Effort**: 2 weeks
**Risk**: High - Touches core business logic
**Files**: `src/services/partner_recipe_plan.py`, `src/services/recipe_slot_assignment.py`

**Problem**:
- Hard-coded partner logic (BlueApron imports)
- Factory pattern implemented incorrectly
- Not scalable for new partners

**Solution**:
```python
# Create partner registry pattern
# src/partners/registry.py
from typing import Dict, Type

class PartnerRegistry:
    """Registry for partner-specific implementations"""

    _recipe_plans: Dict[str, Type['PartnerRecipePlan']] = {}
    _slot_constraints: Dict[str, Type['PartnerSlotConstraints']] = {}

    @classmethod
    def register_recipe_plan(cls, partner_id: str, plan_class: Type['PartnerRecipePlan']):
        cls._recipe_plans[partner_id] = plan_class

    @classmethod
    def get_recipe_plan(cls, partner_id: str) -> Type['PartnerRecipePlan']:
        if partner_id not in cls._recipe_plans:
            raise ValueError(f"No recipe plan registered for partner {partner_id}")
        return cls._recipe_plans[partner_id]

# src/partners/blue_apron.py
from src.partners.registry import PartnerRegistry
from src.services.partner_recipe_plan import PartnerRecipePlan

class BlueApronRecipePlan(PartnerRecipePlan):
    pass

# Register on module load
PartnerRegistry.register_recipe_plan("BA-MAIN", BlueApronRecipePlan)
```

**Implementation Steps**:
1. Create partner registry system
2. Move partner-specific logic to dedicated modules
3. Create configuration-based slot constraints
4. Update factory methods to use registry
5. Add documentation for adding new partners

---

### 2.3 Split Large Service Methods
**Priority**: P1
**Effort**: 1 week
**Risk**: Low - Refactoring without logic changes
**Files**: `src/services/recipe.py`

**Problem**:
- `create_recipe` and `update_recipe` are too large (100+ lines)
- Mix validation, business logic, external calls, error handling
- Hard to test and maintain

**Solution**:
```python
# Break down create_recipe into smaller methods
class RecipeService:

    def create_recipe(self, partner_id: str, recipe_data: CreateRecipeRequest):
        """High-level orchestration method"""
        # Validate
        self._validate_create_request(partner_id, recipe_data)

        # Prepare data
        recipe = self._prepare_recipe_object(partner_id, recipe_data)

        # Assign slot
        slot = self._assign_recipe_slot(recipe)

        # Create in external systems
        culops_id = self._create_in_culops(recipe, slot)

        # Save to cache
        self._save_to_cache(recipe, culops_id)

        # Build response
        return self._build_recipe_response(recipe)

    def _validate_create_request(self, partner_id: str, recipe_data: CreateRecipeRequest):
        """Separate validation logic"""
        self._cycle_date_validator.validate(recipe_data.cycle_date, partner_id, 'create')
        self._validate_tags(partner_id, recipe_data.tags)
        self._validate_pantry_items(recipe_data.pantry_items, recipe_data.cycle_date)

    def _prepare_recipe_object(self, partner_id: str, recipe_data: CreateRecipeRequest) -> Recipe:
        """Separate data preparation"""
        # Build recipe object
        pass
```

**Implementation Steps**:
1. Identify logical sections in large methods
2. Extract each section to private helper method
3. Add unit tests for each helper
4. Update integration tests
5. Document method responsibilities

---

## Phase 3: Medium Priority Improvements (P2) - Weeks 6-8

### 3.1 Reduce Router Repetition with Decorators
**Priority**: P2
**Effort**: 1 week
**Risk**: Low
**Files**: `src/api/routes/v1/recipes/routes.py`

**Problem**:
- Partner validation repeated in every endpoint
- Error handling patterns duplicated

**Solution**:
```python
# src/api/decorators.py
from functools import wraps
from fastapi import Request, Depends

def require_valid_partner(func):
    """Decorator to validate partner ID"""
    @wraps(func)
    async def wrapper(
        request: Request,
        partner: dict = Depends(get_partner),
        partner_service: PartnerService = Depends(get_partner_service),
        *args,
        **kwargs
    ):
        # Validate partner
        partner_service.validate_partner_id(partner["partner_id"])

        # Call original function
        return await func(request, partner, partner_service, *args, **kwargs)

    return wrapper

# Usage in routes
@router.get("/v1/recipes")
@require_valid_partner
async def get_recipes(
    request: Request,
    partner: dict,
    params: GetRecipesParams = Depends(),
    recipe_service: RecipeService = Depends(get_recipe_service)
):
    # No need for validation - decorator handles it
    return recipe_service.get_all_recipes(partner["partner_id"])
```

**Implementation Steps**:
1. Create decorator module
2. Implement partner validation decorator
3. Create error handling decorator
4. Update all route handlers
5. Remove duplicate validation code

---

### 3.2 Centralize Tag Validation
**Priority**: P2
**Effort**: 3 days
**Risk**: Low
**Files**: `src/services/recipe.py`, `src/validators/tag_validator.py`

**Problem**:
- Tag validation duplicated for constraint and packaging tags
- Similar logic repeated in create/update operations

**Solution**:
```python
# src/validators/tag_validator.py
from typing import List, Set
from enum import Enum

class TagType(Enum):
    RECIPE_CONSTRAINT = "recipe_constraint"
    PACKAGING_CONFIG = "packaging_config"

class TagValidator:
    """Centralized tag validation"""

    def __init__(self, partner_repo):
        self._partner_repo = partner_repo
        self._cache = {}  # Cache valid tags per partner

    def validate_tags(
        self,
        partner_id: str,
        tag_ids: List[str],
        tag_type: TagType
    ) -> List[dict]:
        """
        Validate and map tag IDs to tag objects.

        Returns: List of valid tag objects
        Raises: InvalidTagError if any tag is invalid
        """
        valid_tags = self._get_valid_tags(partner_id, tag_type)
        valid_tag_ids = {tag["id"] for tag in valid_tags}

        # Check all provided tags are valid
        invalid_tags = set(tag_ids) - valid_tag_ids
        if invalid_tags:
            raise InvalidTagError(
                f"Invalid {tag_type.value} tags: {invalid_tags}"
            )

        # Return tag objects
        return [tag for tag in valid_tags if tag["id"] in tag_ids]
```

---

### 3.3 Extract Magic Strings to Constants
**Priority**: P2
**Effort**: 2 days
**Risk**: Low
**Files**: All

**Solution**:
```python
# src/constants.py
class ErrorMessages:
    PARTNER_NOT_FOUND = "Partner not found"
    RECIPE_NOT_FOUND = "Recipe not found"
    CYCLE_DATE_INVALID = "Cycle date must be a Monday"
    CYCLE_DATE_PAST = "Cycle date must be in the future"
    WITHIN_CUTOFF = "Cycle date is within cutoff window"
    MIXED_PANTRY_ITEMS = "Cannot mix prepped and ready with standard pantry items"

class HTTPHeaders:
    IDEMPOTENCY_KEY = "Idempotency-Key"
    PARTNER_ID = "X-Partner-ID"

class ReturnOptions:
    RECIPE_ID_SKU_MAPPING = "recipe-id-sku-mapping"

class SlotCodes:
    EXCLUDED_SLOTS = {"F", "FF", "P", "FP", "M", "FM", "V", "FV", "FR", "PX", "MP", "WC"}
```

---

### 3.4 Add Comprehensive Type Hints
**Priority**: P2
**Effort**: 1 week
**Risk**: Low
**Files**: All

**Solution**:
- Add return type hints to all methods
- Use `typing` module for complex types
- Enable mypy strict mode
- Add type checking to CI/CD

---

## Phase 4: Low Priority Improvements (P3) - Weeks 9-10

### 4.1 Add Docstrings and API Documentation
**Priority**: P3
**Effort**: 1 week
**Risk**: None
**Files**: All

**Solution**:
- Add Google-style docstrings to all public methods
- Use FastAPI's `description` and `summary` for endpoints
- Generate OpenAPI documentation
- Create architecture documentation

---

### 4.2 Improve Response Consistency
**Priority**: P3
**Effort**: 3 days
**Risk**: Low - May affect API consumers
**Files**: `src/services/recipe.py`

**Problem**:
- `recipeCardIds` is `[recipe_card_id]` for create, but can be list for get/update
- Inconsistent response shapes

**Solution**:
- Standardize all responses to use consistent field types
- Document breaking changes
- Add API versioning if needed

---

## Testing Strategy

### Unit Tests
- Add tests for all new validators
- Test error paths explicitly
- Aim for 80%+ coverage

### Integration Tests
- Test full request/response cycles
- Validate database interactions
- Test external service integrations

### Performance Tests
- Benchmark before and after N+1 fixes
- Load test with realistic data volumes
- Monitor query execution times

---

## Migration Strategy

### Backward Compatibility
- Maintain existing API contracts during refactoring
- Use feature flags for gradual rollout
- Create deprecation timeline for old patterns

### Rollout Plan
1. Deploy refactored code alongside existing code
2. Route small percentage of traffic to new code
3. Monitor errors and performance
4. Gradually increase traffic to new code
5. Remove old code after full migration

---

## Success Metrics

### Code Quality
- Reduce cyclomatic complexity by 30%
- Achieve 80%+ test coverage
- Zero critical security issues
- Pass all linting checks

### Performance
- 50% reduction in API response times for list operations
- 70% reduction in database queries
- Handle 2x current traffic load

### Maintainability
- New developer onboarding time reduced by 40%
- Time to implement new partner reduced by 60%
- Bug fix time reduced by 30%

---

## Risk Mitigation

### High-Risk Changes
- Partner-specific logic refactoring
- Exception handling changes
- Database query optimization

### Mitigation Strategies
1. Comprehensive test coverage before changes
2. Canary deployments
3. Feature flags for rollback
4. Thorough code review process
5. Performance testing in staging
6. Monitoring and alerting

---

## Timeline Summary

| Phase | Duration | Priority | Key Deliverables |
|-------|----------|----------|------------------|
| 1 | Weeks 1-2 | P0 | Exception handling, cycle date validation |
| 2 | Weeks 3-5 | P1 | N+1 fixes, partner refactoring, method splitting |
| 3 | Weeks 6-8 | P2 | Decorators, tag validation, constants, types |
| 4 | Weeks 9-10 | P3 | Documentation, response consistency |

**Total Estimated Time**: 10 weeks (2.5 months)

---

## Next Steps

1. Review and approve this plan with team
2. Create JIRA tickets for each task
3. Assign owners for each phase
4. Set up project tracking dashboard
5. Begin Phase 1 implementation
