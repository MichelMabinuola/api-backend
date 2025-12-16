from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import json
import logging
from datetime import datetime
from sys_prompt import USER_PROMPT, SYSTEM_PROMPT
from conn import client
from vector_srch import vector_store
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout) 
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Michael's Portfolio RAG API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active connections and their conversation history
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.conversation_history: Dict[str, List[Dict]] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        self.conversation_history[client_id] = []
        logger.info(f"Client {client_id} connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        if client_id in self.conversation_history:
            del self.conversation_history[client_id]
        logger.info(f"Client {client_id} disconnected. Total connections: {len(self.active_connections)}")

    async def send_message(self, message: dict, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_json(message)

    def add_to_history(self, client_id: str, role: str, content: str):
        if client_id not in self.conversation_history:
            self.conversation_history[client_id] = []
        self.conversation_history[client_id].append({
            "role": role,
            "content": content
        })
        # Keep only last 10 messages to manage memory
        if len(self.conversation_history[client_id]) > 10:
            self.conversation_history[client_id] = self.conversation_history[client_id][-10:]

    def get_history(self, client_id: str) -> List[Dict]:
        return self.conversation_history.get(client_id, [])

    def clear_history(self, client_id: str):
        if client_id in self.conversation_history:
            self.conversation_history[client_id] = []

manager = ConnectionManager()

def run_rag(query: str, history: List[Dict] = None) -> str:
    """
    Run RAG pipeline with optional conversation history
    """
    try:
        # 1. Retrieve context from vector store
        context = vector_store(query)
        logger.info(f"Retrieved context for query: {query[:50]}...")

        # 2. Build prompt with context
        formatted_user_prompt = USER_PROMPT.format(context=context, query=query)

        # 3. Build messages with optional history
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Add conversation history if provided (last 5 messages)
        if history:
            messages.extend(history[-5:])
        
        # Add current query
        messages.append({"role": "user", "content": formatted_user_prompt})

        # 4. LLM call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=200
        )

        return response.choices[0].message.content

    except Exception as e:
        logger.error(f"Error in run_rag: {str(e)}")
        raise

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "Michael's Portfolio RAG API with WebSocket is running",
        "active_connections": len(manager.active_connections),
        "timestamp": datetime.now().isoformat()
    }

### this is for different client ids
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """
    WebSocket endpoint for real-time chat
    """
    await manager.connect(websocket, client_id)
    
    try:
        # Send welcome message
        await manager.send_message({
            "type": "system",
            "message": "Connected to RAG chat. You can start asking questions!",
            "timestamp": datetime.now().isoformat()
        }, client_id)

        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            message_type = message_data.get("type", "message")
            user_message = message_data.get("message", "")

            if message_type == "clear":
                # Clear conversation history
                manager.clear_history(client_id)
                await manager.send_message({
                    "type": "system",
                    "message": "Conversation history cleared.",
                    "timestamp": datetime.now().isoformat()
                }, client_id)
                continue

            if not user_message.strip():
                continue

            logger.info(f"Received from {client_id}: {user_message[:50]}...")

            # Add user message to history
            manager.add_to_history(client_id, "user", user_message)

            # Send typing indicator
            await manager.send_message({
                "type": "typing",
                "timestamp": datetime.now().isoformat()
            }, client_id)

            try:
                # Get conversation history
                history = manager.get_history(client_id)

                # Run RAG
                bot_response = run_rag(user_message, history)

                # Add bot response to history
                manager.add_to_history(client_id, "assistant", bot_response)

                # Send response back to client
                await manager.send_message({
                    "type": "message",
                    "message": bot_response,
                    "timestamp": datetime.now().isoformat()
                }, client_id)

            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
                await manager.send_message({
                    "type": "error",
                    "message": "Sorry, I encountered an error processing your request. Please try again.",
                    "timestamp": datetime.now().isoformat()
                }, client_id)

    except WebSocketDisconnect:
        manager.disconnect(client_id)
        logger.info(f"Client {client_id} disconnected")
    except Exception as e:
        logger.error(f"WebSocket error for {client_id}: {str(e)}")
        manager.disconnect(client_id)

@app.get("/stats")
async def get_stats():
    """Get server statistics"""
    return {
        "active_connections": len(manager.active_connections),
        "total_conversations": len(manager.conversation_history),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)