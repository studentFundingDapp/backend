from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
from app.core.database import Database
from app.routes import user_router, project_router, donation_router, auth_router
from typing import Dict, Any

# Initialize FastAPI app without OpenAPI
app = FastAPI(
    title="Decentralized Funding API",
    description="API for decentralized crowdfunding platform",
    version="1.0.0",
    docs_url=None,    # Disable default docs
    redoc_url=None,   # Disable default redoc
    openapi_url=None  # Disable default OpenAPI schema
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for those complaining about CORS
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Database connection events
@app.on_event("startup")
async def startup_db_client():
    await Database.connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await Database.close_mongo_connection()

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(user_router, prefix="/api/users", tags=["users"])
app.include_router(project_router, prefix="/api/projects", tags=["projects"])
app.include_router(donation_router, prefix="/api/donations", tags=["donations"])

# Custom docs endpoints
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="API Docs",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css",
    )

@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_json():
    schema = {
        "openapi": "3.0.2",
        "info": {
            "title": "Decentralized Funding API",
            "version": "1.0.0",
            "description": "API for decentralized crowdfunding platform"
        },
        "paths": {
            "/api/users": {
                "get": {
                    "summary": "List Users",
                    "operationId": "list_users",
                    "tags": ["users"],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/User"}
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "summary": "Create User",
                    "operationId": "create_user",
                    "tags": ["users"],
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/UserCreate"}
                            }
                        },
                        "required": True
                    },
                    "responses": {
                        "201": {
                            "description": "User Created",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/User"}
                                }
                            }
                        }
                    }
                }
            },
            "/api/users/{user_id}": {
                "get": {
                    "summary": "Get User Details",
                    "operationId": "get_user",
                    "tags": ["users"],
                    "parameters": [
                        {
                            "name": "user_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "User Details",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/User"}
                                }
                            }
                        }
                    }
                },
                "put": {
                    "summary": "Update User",
                    "operationId": "update_user",
                    "tags": ["users"],
                    "parameters": [
                        {
                            "name": "user_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ],
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/UserUpdate"}
                            }
                        },
                        "required": True
                    },
                    "responses": {
                        "200": {
                            "description": "User Updated",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/User"}
                                }
                            }
                        }
                    }
                },
                "delete": {
                    "summary": "Delete User",
                    "operationId": "delete_user",
                    "tags": ["users"],
                    "parameters": [
                        {
                            "name": "user_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "204": {
                            "description": "User Deleted"
                        }
                    }
                }
            },
            "/api/projects": {
                "get": {
                    "summary": "List Projects",
                    "operationId": "list_projects",
                    "tags": ["projects"],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Project"}
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "summary": "Create Project",
                    "operationId": "create_project",
                    "tags": ["projects"],
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ProjectBase"}
                            }
                        },
                        "required": True
                    },
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Project"}
                                }
                            }
                        }
                    }
                }
            },
            "/api/projects/{project_id}": {
                "get": {
                    "summary": "Get Project Details",
                    "operationId": "get_project",
                    "tags": ["projects"],
                    "parameters": [
                        {
                            "name": "project_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Project Details",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Project"}
                                }
                            }
                        }
                    }
                },
                "put": {
                    "summary": "Update Project",
                    "operationId": "update_project",
                    "tags": ["projects"],
                    "parameters": [
                        {
                            "name": "project_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ],
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ProjectUpdate"}
                            }
                        },
                        "required": True
                    },
                    "responses": {
                        "200": {
                            "description": "Project Updated",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Project"}
                                }
                            }
                        }
                    }
                },
                "delete": {
                    "summary": "Delete Project",
                    "operationId": "delete_project",
                    "tags": ["projects"],
                    "parameters": [
                        {
                            "name": "project_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "204": {
                            "description": "Project Deleted"
                        }
                    }
                }
            },
            "/api/donations": {
                "get": {
                    "summary": "List Donations",
                    "operationId": "list_donations",
                    "tags": ["donations"],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Transaction"}
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/donations/{donation_id}": {
                "get": {
                    "summary": "Get Donation Details",
                    "operationId": "get_donation",
                    "tags": ["donations"],
                    "parameters": [
                        {
                            "name": "donation_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Donation Details",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Transaction"}
                                }
                            }
                        }
                    }
                },
                "put": {
                    "summary": "Update Donation",
                    "operationId": "update_donation",
                    "tags": ["donations"],
                    "parameters": [
                        {
                            "name": "donation_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ],
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/TransactionUpdate"}
                            }
                        },
                        "required": True
                    },
                    "responses": {
                        "200": {
                            "description": "Donation Updated",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Transaction"}
                                }
                            }
                        }
                    }
                },
                "delete": {
                    "summary": "Delete Donation",
                    "operationId": "delete_donation",
                    "tags": ["donations"],
                    "parameters": [
                        {
                            "name": "donation_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "204": {
                            "description": "Donation Deleted"
                        }
                    }
                }
            },
            "/api/auth/signup": {
                "post": {
                    "summary": "Sign Up",
                    "operationId": "signup",
                    "tags": ["auth"],
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/SignUpRequest"}
                            }
                        },
                        "required": True
                    },
                    "responses": {
                        "201": {
                            "description": "Successfully registered",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/TokenResponse"}
                                }
                            }
                        },
                        "400": {
                            "description": "Bad Request - Email already registered"
                        }
                    }
                }
            },
            "/api/auth/login": {
                "post": {
                    "summary": "Login",
                    "operationId": "login",
                    "tags": ["auth"],
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/LoginRequest"}
                            }
                        },
                        "required": True
                    },
                    "responses": {
                        "200": {
                            "description": "Successfully logged in",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/TokenResponse"}
                                }
                            }
                        },
                        "401": {
                            "description": "Invalid credentials"
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "User": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "email": {"type": "string", "format": "email"},
                        "username": {"type": "string"},
                        "full_name": {"type": "string"},
                        "wallet_address": {"type": "string"},
                        "role": {"type": "string", "enum": ["admin", "donor", "student"]},
                        "created_at": {"type": "string", "format": "date-time"},
                        "updated_at": {"type": "string", "format": "date-time"}
                    },
                    "required": ["email", "username"]
                },
                "UserCreate": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "format": "email"},
                        "username": {"type": "string"},
                        "password": {"type": "string", "format": "password"},
                        "full_name": {"type": "string"},
                        "wallet_address": {"type": "string"},
                        "role": {"type": "string", "enum": ["admin", "donor", "student"]}
                    },
                    "required": ["email", "username", "password"]
                },
                "UserUpdate": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "format": "email"},
                        "username": {"type": "string"},
                        "full_name": {"type": "string"},
                        "wallet_address": {"type": "string"}
                    }
                },
                "Project": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                        "objectives": {"type": "string"},
                        "deliverables": {"type": "string"},
                        "category": {"type": "string"},
                        "target_amount": {"type": "number"},
                        "current_amount": {"type": "number"},
                        "wallet_address": {"type": "string"},
                        "deadline": {"type": "string", "format": "date-time"},
                        "status": {"type": "string", "enum": ["pending", "active", "completed", "cancelled"]},
                        "created_at": {"type": "string", "format": "date-time"},
                        "updated_at": {"type": "string", "format": "date-time"}
                    },
                    "required": ["title", "description", "objectives", "deliverables", "category", "target_amount", "wallet_address", "deadline"]
                },
                "ProjectBase": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                        "objectives": {"type": "string"},
                        "deliverables": {"type": "string"},
                        "category": {"type": "string"},
                        "target_amount": {"type": "number"},
                        "wallet_address": {"type": "string"},
                        "deadline": {"type": "string", "format": "date-time"}
                    },
                    "required": ["title", "description", "objectives", "deliverables", "category", "target_amount", "wallet_address", "deadline"]
                },
                "ProjectUpdate": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                        "objectives": {"type": "string"},
                        "deliverables": {"type": "string"},
                        "category": {"type": "string"},
                        "target_amount": {"type": "number"},
                        "status": {"type": "string", "enum": ["pending", "active", "completed", "cancelled"]}
                    }
                },
                "Transaction": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "amount": {"type": "number"},
                        "transaction_hash": {"type": "string"},
                        "message": {"type": "string"},
                        "asset_type": {"type": "string"},
                        "donor_id": {"type": "string"},
                        "project_id": {"type": "string"},
                        "recipient_wallet": {"type": "string"},
                        "status": {"type": "string"},
                        "created_at": {"type": "string", "format": "date-time"},
                        "block_height": {"type": "integer"},
                        "confirmed_at": {"type": "string", "format": "date-time"}
                    },
                    "required": ["amount", "transaction_hash", "donor_id", "project_id", "recipient_wallet"]
                },
                "TransactionUpdate": {
                    "type": "object",
                    "properties": {
                        "amount": {"type": "number"},
                        "transaction_hash": {"type": "string"},
                        "message": {"type": "string"},
                        "status": {"type": "string"},
                        "block_height": {"type": "integer"},
                        "confirmed_at": {"type": "string", "format": "date-time"}
                    }
                },
                "SignUpRequest": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "format": "email"},
                        "username": {"type": "string"},
                        "password": {"type": "string", "format": "password"},
                        "full_name": {"type": "string"},
                        "wallet_address": {"type": "string"},
                        "role": {"type": "string", "enum": ["admin", "donor", "student"]}
                    },
                    "required": ["email", "username", "password", "role"]
                },
                "LoginRequest": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "format": "email"},
                        "password": {"type": "string", "format": "password"}
                    },
                    "required": ["email", "password"]
                },
                "TokenResponse": {
                    "type": "object",
                    "properties": {
                        "access_token": {"type": "string"},
                        "token_type": {"type": "string"}
                    },
                    "required": ["access_token", "token_type"]
                }
            },
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
        }
    }
    return JSONResponse(content=schema)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}