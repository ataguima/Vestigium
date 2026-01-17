from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class IdentifierType(str, Enum):
    USERNAME = "username"
    EMAIL = "email"
    PHONE = "phone"
    NAME = "name"
    HANDLE = "handle"
    OTHER = "other"


class DecisionChoice(str, Enum):
    YES = "yes"
    NO = "no"
    UNSURE = "unsure"


class HypothesisStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    UNCERTAIN = "uncertain"


@dataclass(frozen=True)
class Evidence:
    source: str
    context: str
    raw_data: Dict[str, Any]
    confidence: float
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=utc_now)


@dataclass(frozen=True)
class Identifier:
    identifier_type: IdentifierType
    value: str
    confidence: float = 0.5
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=utc_now)


@dataclass
class Profile:
    platform: str
    url: str
    identifiers: List[Identifier] = field(default_factory=list)
    evidence: List[Evidence] = field(default_factory=list)
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=utc_now)

    def add_identifier(self, identifier: Identifier) -> None:
        self.identifiers.append(identifier)

    def add_evidence(self, evidence: Evidence) -> None:
        self.evidence.append(evidence)


@dataclass
class Hypothesis:
    description: str
    evidence: List[Evidence] = field(default_factory=list)
    status: HypothesisStatus = HypothesisStatus.PENDING
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def add_evidence(self, evidence: Evidence) -> None:
        self.evidence.append(evidence)
        self.updated_at = utc_now()

    def apply_decision(self, choice: DecisionChoice) -> None:
        if choice == DecisionChoice.YES:
            self.status = HypothesisStatus.ACCEPTED
        elif choice == DecisionChoice.NO:
            self.status = HypothesisStatus.REJECTED
        else:
            self.status = HypothesisStatus.UNCERTAIN
        self.updated_at = utc_now()


@dataclass(frozen=True)
class Decision:
    hypothesis_id: UUID
    choice: DecisionChoice
    rationale: Optional[str] = None
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=utc_now)


@dataclass
class Person:
    display_name: Optional[str] = None
    identifiers: List[Identifier] = field(default_factory=list)
    profiles: List[Profile] = field(default_factory=list)
    evidence: List[Evidence] = field(default_factory=list)
    hypotheses: List[Hypothesis] = field(default_factory=list)
    decisions: List[Decision] = field(default_factory=list)
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=utc_now)

    def add_identifier(self, identifier: Identifier) -> None:
        self.identifiers.append(identifier)

    def add_profile(self, profile: Profile) -> None:
        self.profiles.append(profile)

    def add_evidence(self, evidence: Evidence) -> None:
        self.evidence.append(evidence)

    def add_hypothesis(self, hypothesis: Hypothesis) -> None:
        self.hypotheses.append(hypothesis)

    def record_decision(
        self,
        hypothesis_id: UUID,
        choice: DecisionChoice,
        rationale: Optional[str] = None,
    ) -> Decision:
        decision = Decision(
            hypothesis_id=hypothesis_id,
            choice=choice,
            rationale=rationale,
        )
        self.decisions.append(decision)
        for hypothesis in self.hypotheses:
            if hypothesis.id == hypothesis_id:
                hypothesis.apply_decision(choice)
                break
        return decision

    def get_hypothesis(self, hypothesis_id: UUID) -> Optional[Hypothesis]:
        for hypothesis in self.hypotheses:
            if hypothesis.id == hypothesis_id:
                return hypothesis
        return None
