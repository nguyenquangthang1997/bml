def parse_swagger():
    sample_swagger = {
        "host": "localhost:7999",
        "basePath": "/",
        "swagger": "2.0",
        "schemes": [
            "http"
        ],
        "info": {
            "version": "1",
            "license": {
                "name": "Apache 2.0",
                "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
            },
            "contact": {
                "email": "hust.blockchain@gmail.com"
            },
            "title": "Get data api",
            "description": "identification API"
        },
        "tags": [
            {
                "name": "client",
                "description": "client"
            }
        ],
        "paths": {
            "/get": {
                "post": {
                    "consumes": [
                        "json"
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "summary": "create",
                    "description": "create",
                    "operationId": "create",
                    "responses": {
                        "201": {
                            "description": "created",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "data": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "attribute1": {
                                                    "type": "string"
                                                },
                                                "attribute2": {
                                                    "type": "string"
                                                },
                                                "attribute3": {
                                                    "type": "string"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "invalid input, object invalid"
                        },
                        "409": {
                            "description": "not exist"
                        }
                    },
                    "tags": [
                        "client"
                    ],
                    "parameters": [
                        {
                            "in": "body",
                            "name": "product",
                            "description": "product",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "account": {
                                        "type": "string"
                                    },
                                    "id": {
                                        "type": "string"
                                    },
                                    "filter": {
                                        "type": "array",
                                        "items": {
                                            "type": "string",
                                            "example": "id:int(id)==1"
                                        }
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }
    }
    return sample_swagger
