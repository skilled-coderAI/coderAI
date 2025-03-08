from typing import Dict, Set
from fastapi import WebSocket
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class CollaborationSession:
    document_id: str
    participants: Set[WebSocket] = field(default_factory=set)
    last_modified: datetime = field(default_factory=datetime.now)
    content: str = ""

class CollaborationService:
    def __init__(self):
        self.sessions: Dict[str, CollaborationSession] = {}
    
    async def join_session(self, document_id: str, websocket: WebSocket) -> None:
        """Add a participant to a collaboration session"""
        if document_id not in self.sessions:
            self.sessions[document_id] = CollaborationSession(document_id=document_id)
        await websocket.accept()
        self.sessions[document_id].participants.add(websocket)
    
    async def leave_session(self, document_id: str, websocket: WebSocket) -> None:
        """Remove a participant from a collaboration session"""
        if document_id in self.sessions:
            self.sessions[document_id].participants.remove(websocket)
            if not self.sessions[document_id].participants:
                del self.sessions[document_id]
    
    async def broadcast_changes(self, document_id: str, changes: str, sender: WebSocket) -> None:
        """Broadcast changes to all participants except the sender"""
        if document_id in self.sessions:
            session = self.sessions[document_id]
            session.content = changes
            session.last_modified = datetime.now()
            
            for participant in session.participants:
                if participant != sender:
                    await participant.send_text(changes)
    
    def get_active_sessions(self) -> Dict[str, int]:
        """Get a dictionary of active sessions and their participant counts"""
        return {doc_id: len(session.participants) 
                for doc_id, session in self.sessions.items()}