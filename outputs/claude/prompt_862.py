def get_resource(resource_id):
    resources = {
        "doc1": "Annual Report 2024",
        "doc2": "Meeting Notes",
        "img1": "Profile Photo",
    }
    return resources.get(resource_id, "Resource not found")
