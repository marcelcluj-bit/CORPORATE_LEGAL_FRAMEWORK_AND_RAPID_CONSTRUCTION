"""
Corporate Legal Framework & Rapid Construction Escrow Controller
-----------------------------------------------------------------
Simulates milestone-based fund release for rapid modular construction
and manages state per-inmate daily allowance routing.
"""

import time
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ConstructionMilestone:
    id: int
    description: str
    payout_percentage: float
    is_completed: bool = False
    verification_hash: str = ""


class RapidConstructionEscrow:
    def __init__(self, total_budget_eur: float):
        self.total_budget = total_budget_eur
        self.escrow_balance = total_budget_eur
        self.disbursed_funds = 0.0
        self.facility_operational = False
        
        # Initialize the 4 rapid deployment milestones
        self.milestones: List[ConstructionMilestone] = [
            ConstructionMilestone(1, "Site Prep, Permits & Foundation (Week 1-2)", 0.20),
            ConstructionMilestone(2, "Modular Units Manufacturing & Assembly (Week 3-4)", 0.40),
            ConstructionMilestone(3, "AI Sensor Grid & Utility Integration (Week 5-6)", 0.20),
            ConstructionMilestone(4, "State Reception & Final Commissioning (Week 7-8)", 0.20)
        ]

    def verify_and_release_milestone(self, milestone_id: int, audit_proof_hash: str) -> bool:
        """Verifies phase completion and releases funds from escrow."""
        for ms in self.milestones:
            if ms.id == milestone_id:
                if ms.is_completed:
                    print(f"[ESCROW] Milestone {milestone_id} already released.")
                    return False
                
                ms.is_completed = True
                ms.verification_hash = audit_proof_hash
                release_amount = self.total_budget * ms.payout_percentage
                self.escrow_balance -= release_amount
                self.disbursed_funds += release_amount
                
                print(f"[ESCROW SUCCESS] Milestone {milestone_id} verified ({ms.description}).")
                print(f"                 Released: €{release_amount:,.2f} | Remaining Escrow: €{self.escrow_balance:,.2f}")
                
                if milestone_id == 4:
                    self.facility_operational = True
                    print("\n[STATE ACTIVATION] Facility fully received by state authorities! Operational mode ACTIVE.\n")
                return True
        return False


class StateAllowanceProcessor:
    def __init__(self, daily_per_inmate_eur: float, total_inmates: int):
        self.daily_rate = daily_per_inmate_eur
        self.total_inmates = total_inmates
        self.total_state_funds_received = 0.0
        self.buyback_pool_eur = 0.0
        self.operations_pool_eur = 0.0

    def process_daily_disbursement(self, buyback_ratio: float = 0.25) -> Dict[str, float]:
        """Processes state allowance and routes funds for token buyback & operations."""
        daily_total = self.daily_rate * self.total_inmates
        self.total_state_funds_received += daily_total
        
        buyback_allocation = daily_total * buyback_ratio
        ops_allocation = daily_total * (1.0 - buyback_ratio)
        
        self.buyback_pool_eur += buyback_allocation
        self.operations_pool_eur += ops_allocation
        
        return {
            "daily_total": daily_total,
            "buyback_allocation": buyback_allocation,
            "operations_allocation": ops_allocation
        }


# --- EXECUTION DEMO ---
if __name__ == "__main__":
    print("=" * 70)
    print("   RAPID CONSTRUCTION ESCROW & RWA STATE ALLOWANCE PROTOCOL")
    print("=" * 70)
    
    # Initialize €12 Million Construction Project
    escrow = RapidConstructionEscrow(total_budget_eur=12_000_000.0)
    
    print(f"\nInitial Project Escrow Budget: €{escrow.total_budget:,.2f}\n")
    
    # Simulate Rapid Construction Weeks
    escrow.verify_and_release_milestone(1, "0x9a8f...foundation_ok")
    escrow.verify_and_release_milestone(2, "0x4b1c...assembly_ok")
    escrow.verify_and_release_milestone(3, "0x7e2d...ai_grid_ok")
    escrow.verify_and_release_milestone(4, "0x1f3a...state_reception_ok")
    
    # If facility is operational, start processing state daily allowance (e.g., €45/day per inmate for 500 inmates)
    if escrow.facility_operational:
        processor = StateAllowanceProcessor(daily_per_inmate_eur=45.0, total_inmates=500)
        daily_summary = processor.process_daily_disbursement(buyback_ratio=0.30)
        
        print("-" * 70)
        print("DAILY STATE ALLOWANCE DISTRIBUTION SUMMARY")
        print("-" * 70)
        print(f"Capacity: {processor.total_inmates} inmates @ €{processor.daily_rate}/day")
        print(f"Total Daily State Payment: €{daily_summary['daily_total']:,.2f}")
        print(f" -> Allocated to Token Buyback & Burn (30%): €{daily_summary['buyback_allocation']:,.2f}")
        print(f" -> Allocated to Campus Operations (70%):     €{daily_summary['operations_allocation']:,.2f}")
        print("=" * 70)
