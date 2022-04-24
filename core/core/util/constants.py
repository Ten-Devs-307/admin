from enum import Enum


class Status(Enum):
    APPROVED = 'approved'
    PENDING = 'pending'
    REJECTED = 'rejected'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    SUCCESSFUL = 'successful'
    FAILED = 'failed'


class Disbursement(Enum):
    CREDIT = 'credit'
    DEBIT = 'debit'
    CASHOUT = 'cashout'


class Reason(Enum):
    INSUFFICIENT_BALANCE = 'insufficient balance'
    CASHOUT_SUCCESSFUL = 'cashout successful'
