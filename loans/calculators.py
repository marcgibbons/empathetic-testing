import numpy as np
import numpy_financial as npf


def get_amortization_schedule(principal, rate, number_of_periods):
    if not number_of_periods:
        return []

    pv = principal
    nper = number_of_periods

    per = get_per(number_of_periods)
    interest_paid = get_interest_paid(rate, per, nper, pv)
    principal_paid = get_principal_paid(rate, per, nper, pv)
    payment = get_payment(interest_paid, principal_paid)
    balance = get_balance(principal, principal_paid)

    return [
        {
            "balance": balance[i],
            "interest": interest_paid[i],
            "payment": payment[i],
            "principal": principal_paid[i],
        }
        for i in range(number_of_periods)
    ]


def get_per(number_of_periods):
    return np.arange(number_of_periods) + 1


def get_interest_paid(rate, per, nper, pv):
    return -np.round(npf.ipmt(rate=rate, per=per, nper=nper, pv=pv), 2)


def get_principal_paid(rate, per, nper, pv):
    return -np.round(npf.ppmt(rate=rate, per=per, nper=nper, pv=pv), 2)


def get_payment(interest_paid, principal_paid):
    return np.round(interest_paid + principal_paid, 2)


def get_balance(principal, principal_paid):
    return principal - principal_paid.cumsum()
