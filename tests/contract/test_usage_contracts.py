from uuid import uuid4

import pytest
from pydantic import ValidationError

from core.contracts import (
    EntitlementKey,
    PlanRef,
    TaskComplexity,
    TaskUnitCost,
    UsageEstimate,
    UsageReservation,
    UsageReservationStatus,
    UsageSettlement,
    export_contract_schemas,
)


def test_plan_and_task_unit_cost_contracts_are_schema_exportable():
    plan = PlanRef(
        plan_id="pro",
        display_name="Pro",
        task_unit_limit=100,
        entitlements={EntitlementKey.AGENT_MODE, EntitlementKey.GITHUB_READ},
    )
    cost = TaskUnitCost(complexity=TaskComplexity.COMPLEX, units=3)

    assert EntitlementKey.AGENT_MODE in plan.entitlements
    assert cost.units == 3
    assert "PlanRef" in export_contract_schemas()
    assert "UsageEstimate" in export_contract_schemas()


def test_estimate_reserve_settle_lifecycle_contracts():
    tenant_id = uuid4()
    execution_id = uuid4()
    reservation_id = uuid4()

    estimate = UsageEstimate(
        tenant_id=tenant_id,
        complexity=TaskComplexity.MEDIUM,
        estimated_units=2,
        cost_snapshot={"policy_version": "v1"},
    )
    reservation = UsageReservation(
        reservation_id=reservation_id,
        tenant_id=tenant_id,
        execution_id=execution_id,
        units_reserved=estimate.estimated_units,
        cost_snapshot=estimate.cost_snapshot,
    )
    settlement = UsageSettlement(
        reservation_id=reservation_id,
        execution_id=execution_id,
        units_reserved=reservation.units_reserved,
        units_settled=2,
        status=UsageReservationStatus.SETTLED,
    )

    assert reservation.status == UsageReservationStatus.RESERVED
    assert settlement.units_settled == estimate.estimated_units


def test_settlement_rejects_over_settlement_or_non_final_status():
    with pytest.raises(ValidationError):
        UsageSettlement(
            reservation_id=uuid4(),
            execution_id=uuid4(),
            units_reserved=2,
            units_settled=3,
            status=UsageReservationStatus.SETTLED,
        )

    with pytest.raises(ValidationError):
        UsageSettlement(
            reservation_id=uuid4(),
            execution_id=uuid4(),
            units_reserved=2,
            units_settled=1,
            status=UsageReservationStatus.RESERVED,
        )
