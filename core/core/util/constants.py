from enum import Enum


class Status(Enum):
    APPROVED = 'approved'
    PENDING = 'pending'
    REJECTED = 'rejected'


class Disbursement(Enum):
    CREDIT = 'credit'
    DEBIT = 'debit'