from __future__ import annotations

import json
import pkgutil
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping


ROOM_GRAPH_SCHEMA_VERSION = 2
ROOM_GRAPH_RESOURCE = "room_graph_data.json"


class RequirementMode(str, Enum):
    INHERIT = "inherit"
    NONE = "none"
    EXPRESSION = "expression"
    UNRESOLVED = "unresolved"


class LogicStatus(str, Enum):
    ACTIVE = "active"
    UNRESOLVED = "unresolved"


@dataclass(frozen=True)
class RequirementSpec:
    raw: str
    mode: RequirementMode
    dnf: tuple[tuple[str, ...], ...]
    annotations: tuple[str, ...]
    unresolved_reasons: tuple[str, ...]
    minimum_skip_tier: int

    @property
    def is_compilable(self) -> bool:
        return self.mode is not RequirementMode.UNRESOLVED

    @property
    def inherits_node_access(self) -> bool:
        return self.mode is RequirementMode.INHERIT


@dataclass(frozen=True)
class GraphNode:
    id: str
    name: str
    declared: bool


@dataclass(frozen=True)
class TransitionTarget:
    raw: str
    room_id: str | None
    alias: str | None
    port_id: str | None
    label: str | None


@dataclass(frozen=True)
class RoomTransition:
    id: str
    alias: str
    name: str
    source_node_id: str | None
    target: TransitionTarget
    requirement: RequirementSpec
    notes: str
    source_line: int
    raw_cells: Mapping[str, str]
    status: LogicStatus
    unresolved_reasons: tuple[str, ...]

    @property
    def is_compilable(self) -> bool:
        return self.status is LogicStatus.ACTIVE and self.requirement.is_compilable


@dataclass(frozen=True)
class SubroomConnection:
    id: str
    alias: str
    name: str
    source_node_id: str | None
    target_node_id: str | None
    requirement: RequirementSpec
    notes: str
    source_line: int
    raw_cells: Mapping[str, str]
    status: LogicStatus
    unresolved_reasons: tuple[str, ...]

    @property
    def is_compilable(self) -> bool:
        return self.status is LogicStatus.ACTIVE and self.requirement.is_compilable


@dataclass(frozen=True)
class GraphEvent:
    id: str
    label: str
    kind: str
    node_id: str | None
    requirement: RequirementSpec
    notes: str
    source_line: int
    raw_cells: Mapping[str, str]
    status: LogicStatus
    unresolved_reasons: tuple[str, ...]

    @property
    def is_compilable(self) -> bool:
        return self.status is LogicStatus.ACTIVE and self.requirement.is_compilable


@dataclass(frozen=True)
class CheckAssignment:
    id: str
    label: str
    canonical_location: str | None
    canonical_mapping_confidence: str | None
    node_id: str | None
    requirement: RequirementSpec
    notes: str
    currently_randomized: bool
    source_line: int
    raw_cells: Mapping[str, str]
    status: LogicStatus
    unresolved_reasons: tuple[str, ...]

    @property
    def is_compilable(self) -> bool:
        return (
            self.status is LogicStatus.ACTIVE
            and self.requirement.is_compilable
            and self.canonical_location is not None
        )


@dataclass(frozen=True)
class RoomDefinition:
    id: str
    area_id: str
    name: str
    source_file: str
    source_sha256: str
    geometry_act_independent: bool
    notes: str
    nodes: tuple[GraphNode, ...]
    transitions: tuple[RoomTransition, ...]
    connections: tuple[SubroomConnection, ...]
    events: tuple[GraphEvent, ...]
    checks: tuple[CheckAssignment, ...]
    omitted_check_rows: tuple[Mapping[str, Any], ...]


@dataclass(frozen=True)
class RoomGraph:
    schema_version: int
    source_name: str
    source_document_count: int
    source_aggregate_sha256: str
    assumptions: Mapping[str, Any]
    areas: tuple[str, ...]
    authoritative_areas: frozenset[str]
    metadata_only_areas: frozenset[str]
    rooms: tuple[RoomDefinition, ...]

    def is_authoritative_room(self, room: RoomDefinition) -> bool:
        return room.area_id in self.authoritative_areas

    @property
    def authoritative_rooms(self) -> tuple[RoomDefinition, ...]:
        return tuple(room for room in self.rooms if self.is_authoritative_room(room))

    @property
    def room_by_id(self) -> Mapping[str, RoomDefinition]:
        return MappingProxyType({room.id: room for room in self.rooms})

    @property
    def node_by_id(self) -> Mapping[str, GraphNode]:
        return MappingProxyType(
            {node.id: node for room in self.rooms for node in room.nodes}
        )

    @property
    def transition_by_id(self) -> Mapping[str, RoomTransition]:
        return MappingProxyType(
            {
                transition.id: transition
                for room in self.rooms
                for transition in room.transitions
            }
        )

    @property
    def connection_by_id(self) -> Mapping[str, SubroomConnection]:
        return MappingProxyType(
            {
                connection.id: connection
                for room in self.rooms
                for connection in room.connections
            }
        )

    @property
    def check_by_id(self) -> Mapping[str, CheckAssignment]:
        return MappingProxyType(
            {check.id: check for room in self.rooms for check in room.checks}
        )

    @property
    def event_by_id(self) -> Mapping[str, GraphEvent]:
        return MappingProxyType(
            {event.id: event for room in self.rooms for event in room.events}
        )

    @property
    def compilable_checks(self) -> tuple[CheckAssignment, ...]:
        return tuple(
            check
            for room in self.authoritative_rooms
            for check in room.checks
            if check.is_compilable and check.currently_randomized
        )

    def validation_errors(self) -> tuple[str, ...]:
        errors: list[str] = []
        if self.authoritative_areas & self.metadata_only_areas:
            errors.append("authoritative and metadata-only areas overlap")
        if set(self.areas) != self.authoritative_areas | self.metadata_only_areas:
            errors.append("area authority sets do not cover the imported areas")
        room_ids = [room.id for room in self.rooms]
        if len(room_ids) != len(set(room_ids)):
            errors.append("duplicate room id")
        node_ids = [node.id for room in self.rooms for node in room.nodes]
        if len(node_ids) != len(set(node_ids)):
            errors.append("duplicate node id")
        transition_ids = [
            transition.id
            for room in self.rooms
            for transition in room.transitions
        ]
        if len(transition_ids) != len(set(transition_ids)):
            errors.append("duplicate transition id")
        connection_ids = [
            connection.id
            for room in self.rooms
            for connection in room.connections
        ]
        if len(connection_ids) != len(set(connection_ids)):
            errors.append("duplicate connection id")
        check_ids = [check.id for room in self.rooms for check in room.checks]
        if len(check_ids) != len(set(check_ids)):
            errors.append("duplicate check id")
        event_ids = [event.id for room in self.rooms for event in room.events]
        if len(event_ids) != len(set(event_ids)):
            errors.append("duplicate event id")

        known_rooms = set(room_ids)
        known_nodes = set(node_ids)
        known_ports = set(transition_ids)
        for room in self.rooms:
            if not room.geometry_act_independent:
                errors.append(f"{room.id}: geometry is unexpectedly act-dependent")
            for transition in room.transitions:
                if transition.status is LogicStatus.ACTIVE:
                    if transition.source_node_id not in known_nodes:
                        errors.append(f"{transition.id}: active transition has unknown source node")
                    if transition.target.room_id not in known_rooms:
                        errors.append(f"{transition.id}: active transition has unknown target room")
                    if transition.target.port_id not in known_ports:
                        errors.append(f"{transition.id}: active transition has unknown target port")
                    if not transition.requirement.is_compilable:
                        errors.append(f"{transition.id}: active transition has unresolved requirement")
            for connection in room.connections:
                if connection.status is LogicStatus.ACTIVE:
                    if connection.source_node_id not in known_nodes:
                        errors.append(f"{connection.id}: active connection has unknown source node")
                    if connection.target_node_id not in known_nodes:
                        errors.append(f"{connection.id}: active connection has unknown target node")
                    if not connection.requirement.is_compilable:
                        errors.append(f"{connection.id}: active connection has unresolved requirement")
            for event in room.events:
                if event.status is LogicStatus.ACTIVE:
                    if event.node_id not in known_nodes:
                        errors.append(f"{event.id}: active event has unknown node")
                    if not event.requirement.is_compilable:
                        errors.append(f"{event.id}: active event has unresolved requirement")
            for check in room.checks:
                if check.status is LogicStatus.ACTIVE:
                    if check.node_id not in known_nodes:
                        errors.append(f"{check.id}: active check has unknown node")
                    if not check.requirement.is_compilable:
                        errors.append(f"{check.id}: active check has unresolved requirement")
        return tuple(errors)


def _mapping(value: Mapping[str, Any]) -> Mapping[str, Any]:
    return MappingProxyType(dict(value))


def _requirement_from_json(value: Mapping[str, Any]) -> RequirementSpec:
    minimum_skip_tier = int(value["minimum_skip_tier"])
    if minimum_skip_tier not in range(4):
        raise ValueError(
            f"minimum_skip_tier must be between 0 and 3, got {minimum_skip_tier}"
        )
    return RequirementSpec(
        raw=str(value["raw"]),
        mode=RequirementMode(value["mode"]),
        dnf=tuple(tuple(str(atom) for atom in clause) for clause in value["dnf"]),
        annotations=tuple(str(note) for note in value["annotations"]),
        unresolved_reasons=tuple(str(reason) for reason in value["unresolved_reasons"]),
        minimum_skip_tier=minimum_skip_tier,
    )


def _status(value: Mapping[str, Any]) -> LogicStatus:
    return LogicStatus(value["logic_status"])


def _room_from_json(value: Mapping[str, Any]) -> RoomDefinition:
    return RoomDefinition(
        id=str(value["id"]),
        area_id=str(value["area_id"]),
        name=str(value["name"]),
        source_file=str(value["source_file"]),
        source_sha256=str(value["source_sha256"]),
        geometry_act_independent=bool(value["geometry_act_independent"]),
        notes=str(value["notes"]),
        nodes=tuple(
            GraphNode(
                id=str(node["id"]),
                name=str(node["name"]),
                declared=bool(node["declared"]),
            )
            for node in value["nodes"]
        ),
        transitions=tuple(
            RoomTransition(
                id=str(row["id"]),
                alias=str(row["alias"]),
                name=str(row["name"]),
                source_node_id=row["source_node_id"],
                target=TransitionTarget(
                    raw=str(row["target"]["raw"]),
                    room_id=row["target"]["room_id"],
                    alias=row["target"]["alias"],
                    port_id=row["target"]["port_id"],
                    label=row["target"]["label"],
                ),
                requirement=_requirement_from_json(row["requirement"]),
                notes=str(row["notes"]),
                source_line=int(row["source_line"]),
                raw_cells=_mapping(row["raw_cells"]),
                status=_status(row),
                unresolved_reasons=tuple(row["unresolved_reasons"]),
            )
            for row in value["transitions"]
        ),
        connections=tuple(
            SubroomConnection(
                id=str(row["id"]),
                alias=str(row["alias"]),
                name=str(row["name"]),
                source_node_id=row["source_node_id"],
                target_node_id=row["target_node_id"],
                requirement=_requirement_from_json(row["requirement"]),
                notes=str(row["notes"]),
                source_line=int(row["source_line"]),
                raw_cells=_mapping(row["raw_cells"]),
                status=_status(row),
                unresolved_reasons=tuple(row["unresolved_reasons"]),
            )
            for row in value["connections"]
        ),
        events=tuple(
            GraphEvent(
                id=str(row["id"]),
                label=str(row["label"]),
                kind=str(row["kind"]),
                node_id=row["node_id"],
                requirement=_requirement_from_json(row["requirement"]),
                notes=str(row["notes"]),
                source_line=int(row["source_line"]),
                raw_cells=_mapping(row["raw_cells"]),
                status=_status(row),
                unresolved_reasons=tuple(row["unresolved_reasons"]),
            )
            for row in value["events"]
        ),
        checks=tuple(
            CheckAssignment(
                id=str(row["id"]),
                label=str(row["label"]),
                canonical_location=row["canonical_location"],
                canonical_mapping_confidence=row["canonical_mapping_confidence"],
                node_id=row["node_id"],
                requirement=_requirement_from_json(row["requirement"]),
                notes=str(row["notes"]),
                currently_randomized=bool(row["currently_randomized"]),
                source_line=int(row["source_line"]),
                raw_cells=_mapping(row["raw_cells"]),
                status=_status(row),
                unresolved_reasons=tuple(row["unresolved_reasons"]),
            )
            for row in value["checks"]
        ),
        omitted_check_rows=tuple(_mapping(row) for row in value["omitted_check_rows"]),
    )


@lru_cache(maxsize=1)
def load_room_graph() -> RoomGraph:
    try:
        payload = pkgutil.get_data(__package__, ROOM_GRAPH_RESOURCE)
    except (ImportError, ValueError):
        payload = Path(__file__).with_name(ROOM_GRAPH_RESOURCE).read_bytes()
    if payload is None:
        raise FileNotFoundError(f"missing packaged room graph resource: {ROOM_GRAPH_RESOURCE}")
    return parse_room_graph(json.loads(payload.decode("utf-8")))


def parse_room_graph(value: Mapping[str, Any]) -> RoomGraph:
    schema_version = int(value["schema_version"])
    if schema_version != ROOM_GRAPH_SCHEMA_VERSION:
        raise ValueError(
            f"unsupported room graph schema {schema_version}. "
            f"Expected {ROOM_GRAPH_SCHEMA_VERSION}"
        )
    source = value["source"]
    graph = RoomGraph(
        schema_version=schema_version,
        source_name=str(source["name"]),
        source_document_count=int(source["document_count"]),
        source_aggregate_sha256=str(source["aggregate_sha256"]),
        assumptions=_mapping(value["assumptions"]),
        areas=tuple(str(area) for area in value["areas"]),
        authoritative_areas=frozenset(
            str(area) for area in value["authoritative_areas"]
        ),
        metadata_only_areas=frozenset(
            str(area) for area in value["metadata_only_areas"]
        ),
        rooms=tuple(_room_from_json(room) for room in value["rooms"]),
    )
    errors = graph.validation_errors()
    if errors:
        raise ValueError("invalid room graph: " + " | ".join(errors))
    return graph
