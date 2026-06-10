"""normalize risk levels to Critical/Major/Minor and drop In Progress status

Revision ID: b8c0d2e4f6a8
Revises: a7p9q1r3s5t7
Create Date: 2026-06-10

Maps HSE daily level_risiko Rendah/Sedang/Tinggi -> Minor/Major/Critical,
migrates legacy 'In Progress' inspections to 'Progress Validasi' and any
'In Progress' case incidents to 'Open', then tightens the check constraints.
"""
from alembic import op
import sqlalchemy as sa

revision = 'b8c0d2e4f6a8'
down_revision = 'a7p9q1r3s5t7'
branch_labels = None
depends_on = None


def upgrade():
    # NOTE: drop each check constraint BEFORE converting data, since the new
    # values are not permitted by the old constraint, then re-add it after.

    # ── HSE daily level_risiko: Rendah/Sedang/Tinggi -> Minor/Major/Critical ──
    op.drop_constraint('reports_hse_daily_level_risiko_check', 'reports_hse_daily', type_='check')
    op.execute("UPDATE reports_hse_daily SET level_risiko = 'Minor' WHERE level_risiko = 'Rendah'")
    op.execute("UPDATE reports_hse_daily SET level_risiko = 'Major' WHERE level_risiko = 'Sedang'")
    op.execute("UPDATE reports_hse_daily SET level_risiko = 'Critical' WHERE level_risiko = 'Tinggi'")
    op.create_check_constraint(
        'reports_hse_daily_level_risiko_check',
        'reports_hse_daily',
        "level_risiko IN ('Minor', 'Major', 'Critical')",
    )

    # ── Inspection K3L: legacy 'In Progress' -> 'Progress Validasi' ──
    op.drop_constraint('reports_inspectionk3l_status_check', 'reports_inspectionk3l', type_='check')
    op.execute("UPDATE reports_inspectionk3l SET status = 'Progress Validasi' WHERE status = 'In Progress'")
    op.create_check_constraint(
        'reports_inspectionk3l_status_check',
        'reports_inspectionk3l',
        "status IN ('Open', 'Closed', 'Progress Validasi')",
    )

    # ── Case incidents: legacy 'In Progress' -> 'Open' (no validation stage) ──
    op.drop_constraint('case_incidents_status_check', 'report_case_incidents', type_='check')
    op.execute("UPDATE report_case_incidents SET status = 'Open' WHERE status = 'In Progress'")
    op.create_check_constraint(
        'case_incidents_status_check',
        'report_case_incidents',
        "status IN ('Open', 'Closed')",
    )


def downgrade():
    # Case incidents: restore looser constraint (data revert not possible)
    op.drop_constraint('case_incidents_status_check', 'report_case_incidents', type_='check')
    op.create_check_constraint(
        'case_incidents_status_check',
        'report_case_incidents',
        "status IN ('Open', 'In Progress', 'Closed')",
    )

    # Inspection K3L: restore previous constraint (Progress Validasi rows kept)
    op.drop_constraint('reports_inspectionk3l_status_check', 'reports_inspectionk3l', type_='check')
    op.create_check_constraint(
        'reports_inspectionk3l_status_check',
        'reports_inspectionk3l',
        "status IN ('Open', 'In Progress', 'Closed', 'Progress Validasi')",
    )

    # HSE daily level_risiko: Minor/Major/Critical -> Rendah/Sedang/Tinggi
    op.drop_constraint('reports_hse_daily_level_risiko_check', 'reports_hse_daily', type_='check')
    op.execute("UPDATE reports_hse_daily SET level_risiko = 'Rendah' WHERE level_risiko = 'Minor'")
    op.execute("UPDATE reports_hse_daily SET level_risiko = 'Sedang' WHERE level_risiko = 'Major'")
    op.execute("UPDATE reports_hse_daily SET level_risiko = 'Tinggi' WHERE level_risiko = 'Critical'")
    op.create_check_constraint(
        'reports_hse_daily_level_risiko_check',
        'reports_hse_daily',
        "level_risiko IN ('Rendah', 'Sedang', 'Tinggi')",
    )
