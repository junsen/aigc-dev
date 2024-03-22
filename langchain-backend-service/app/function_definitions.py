functions = [
    {
        "name": "get_customer_info",
        "description": "Get the name list of IRM's customer",
    },
    {
        "name": "create_review",
        "description": "Create a review for the IRM",
        "parameters": {
            "type": "object",
            "properties": {
                "review_text": {
                    "type": "string",
                    "description": "The text of the review, e.g. Great IRM!",
                },
            },
            "required": ["review_text"],
        },
    },
    {
        "name": "ask_vector_db",
        "description": "Ask any question related to IRM. This can include queries about administrator guide for settings.",
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The question to ask, e.g. 'How to manage brands?'",
                },
            },
            "required": ["question"],
        },
    },
    {
        "name": "search_in_sap_docs",
        "description": "Search question in SAP help docs website.",
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The question to ask, e.g. 'Datasphere'",
                },
            },
            "required": ["question"],
        },
    },
]
