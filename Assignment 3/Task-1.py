from dataclasses import dataclass
from typing import Optional

@dataclass
class Inputs:
    prev_reading: float
    curr_reading: float
    customer_type: str
    load_kw: float
    phase_type: str
    eligible_free_200: bool
    fsa_rate: Optional[float] = 0.0

def validate_inputs(inputs: Inputs) -> bool:
    """Validate all input parameters."""
    if inputs.curr_reading < inputs.prev_reading:
        print("Error: Current reading cannot be less than previous reading!")
        return False
    
    if inputs.customer_type.lower() not in ['domestic', 'commercial']:
        print("Error: Customer type must be 'domestic' or 'commercial'!")
        return False
    
    if inputs.load_kw <= 0:
        print("Error: Contracted load must be positive!")
        return False
    
    if inputs.phase_type.lower() not in ['single', 'three']:
        print("Error: Phase type must be 'single' or 'three'!")
        return False
    
    return True

def energy_charges_domestic(units: float) -> float:
    """Calculate energy charges for domestic consumers."""
    slabs = [
        (50, 1.95),
        (100, 3.10),
        (200, 4.80),
        (300, 7.70),
        (400, 9.00),
        (800, 9.50),
        (float('inf'), 10.00)
    ]
    
    total_charge = 0
    remaining_units = units
    prev_slab = 0
    
    for slab, rate in slabs:
        units_in_slab = min(remaining_units, slab - prev_slab)
        if units_in_slab <= 0:
            break
        total_charge += units_in_slab * rate
        remaining_units -= units_in_slab
        prev_slab = slab
    
    return total_charge

def energy_charges_commercial(units: float) -> float:
    """Calculate energy charges for commercial consumers."""
    slabs = [
        (50, 7.00),
        (100, 8.50),
        (300, 9.90),
        (500, 10.40),
        (float('inf'), 11.00)
    ]
    
    total_charge = 0
    remaining_units = units
    prev_slab = 0
    
    for slab, rate in slabs:
        units_in_slab = min(remaining_units, slab - prev_slab)
        if units_in_slab <= 0:
            break
        total_charge += units_in_slab * rate
        remaining_units -= units_in_slab
        prev_slab = slab
    
    return total_charge

def fixed_charges_rs(cust_type: str, load_kw: float, units: float) -> float:
    """Calculate fixed charges."""
    if cust_type.lower() == 'domestic':
        return 10 * load_kw
    else:  # commercial
        return 60 * load_kw if units <= 50 else 70 * load_kw

def customer_charges_rs(cust_type: str, phase: str, load_kw: float) -> float:
    """Calculate customer charges."""
    if cust_type.lower() == 'domestic':
        if phase.lower() == 'three':
            return 150
        else:  # single phase
            return 25 if load_kw <= 1 else 50
    else:  # commercial
        return 200 if phase.lower() == 'three' else 65

def get_user_inputs() -> Inputs:
    """Get all required inputs from user."""
    try:
        prev_reading = float(input("Enter previous reading (PU): "))
        curr_reading = float(input("Enter current reading (CU): "))
        cust_type = input("Enter customer type (domestic/commercial): ").lower()
        load_kw = float(input("Enter contracted load in kW: "))
        phase = input("Enter phase type (single/three): ").lower()
        eligible = input("Eligible for free-200-units scheme? (Y/N): ").upper() == 'Y'
        
        fsa_input = input("Enter FSA rate (₹/unit) [Press Enter for 0]: ").strip()
        fsa_rate = float(fsa_input) if fsa_input else 0.0
        
        return Inputs(
            prev_reading=prev_reading,
            curr_reading=curr_reading,
            customer_type=cust_type,
            load_kw=load_kw,
            phase_type=phase,
            eligible_free_200=eligible,
            fsa_rate=fsa_rate
        )
    except ValueError as e:
        print(f"Error: Invalid input! Please enter numeric values where required.")
        exit(1)

def compute_bill(inputs: Inputs) -> dict:
    """Compute all bill components and return as dictionary."""
    units = inputs.curr_reading - inputs.prev_reading
    
    # Check for negative units
    if units < 0:
        print("Error: Negative units consumed!")
        exit(1)
    
    # Check for free-200-units scheme
    if (inputs.eligible_free_200 and 
        inputs.customer_type == 'domestic' and 
        units <= 200):
        return {
            'units': units,
            'ec': 0,
            'fc': 0,
            'cc': 0,
            'ed': 0,
            'fsa': 0,
            'total': 0
        }
    
    # Calculate each component
    ec = (energy_charges_domestic(units) 
          if inputs.customer_type == 'domestic' 
          else energy_charges_commercial(units))
    
    fc = fixed_charges_rs(inputs.customer_type, inputs.load_kw, units)
    cc = customer_charges_rs(inputs.customer_type, inputs.phase_type, inputs.load_kw)
    ed = 0.06 * units  # Electricity duty
    fsa = units * inputs.fsa_rate if inputs.fsa_rate else 0
    
    total = ec + fc + cc + ed + fsa
    
    return {
        'units': units,
        'ec': ec,
        'fc': fc,
        'cc': cc,
        'ed': ed,
        'fsa': fsa,
        'total': total
    }

def print_bill(bill: dict):
    """Print the bill in the specified format."""
    if bill['total'] == 0:
        print("\nNo Bill under Free 200 Units Scheme")
        return
    
    print(f"\nUnits: {bill['units']:.2f} kWh")
    print(f"EC (Energy Charges): ₹{bill['ec']:.2f}")
    print(f"FC (Fixed Charges):  ₹{bill['fc']:.2f}")
    print(f"CC (Customer Chg):   ₹{bill['cc']:.2f}")
    print(f"ED (Elec. Duty):     ₹{bill['ed']:.2f}")
    print(f"FSA:                 ₹{bill['fsa']:.2f}")
    print(f"TOTAL BILL:          ₹{bill['total']:.2f}")

def main():
    """Main program execution."""
    print("TGNPDCL Electricity Bill Calculator")
    print("-" * 35)
    
    # Get user inputs
    inputs = get_user_inputs()
    
    # Validate inputs
    if not validate_inputs(inputs):
        exit(1)
    
    # Compute and print bill
    bill = compute_bill(inputs)
    print_bill(bill)

if __name__ == "__main__":
    main()
