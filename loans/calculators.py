import numpy as np
import numpy_financial as npf
import pandas as pd


def get_amortization_schedule(principal, rate, number_of_periods):
    if not number_of_periods:
        return []

    npf_kwargs = {
        "nper": number_of_periods,
        "per": np.arange(number_of_periods) + 1,
        "pv": principal,
        "rate": rate,
    }
    principal_paid = -npf.ppmt(**npf_kwargs)
    interest_paid = -npf.ipmt(**npf_kwargs)

    df = pd.DataFrame(
        {
            "balance": principal - principal_paid.cumsum(),
            "interest": interest_paid,
            "principal": principal_paid,
            "payment": interest_paid + principal_paid,
        }
    )
    return df.to_dict("records")
