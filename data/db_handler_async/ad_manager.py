from .db_sync_utils import execute_query, execute_mutation
from .files import delete_file_from_storage_by_url
from .general_function import get_chosen_orgs


def get_organizations_db():
    orgs_query = "SELECT * FROM organization ORDER BY created_at DESC"
    organizations = execute_query(orgs_query)
    
    if not organizations:
        return []

    # Get ad counts for each organization
    for org in organizations:
        # Use the organization name to count ads
        count_query = "SELECT COUNT(*) as count FROM ads WHERE organization = $1"
        count_result = execute_query(count_query, (org.get("organization"),))
        org["ad_count"] = count_result[0]["count"] if count_result else 0
        
    return organizations


def add_organization_db(data):
    try:
        # Case-insensitive check for existing organization
        existing_org_query = "SELECT id FROM organization WHERE LOWER(organization) = LOWER($1)"
        existing_org_result = execute_query(existing_org_query, (data['organization'],))
        if existing_org_result:
            return {"status": "error", "message": "An organization with this name already exists."}
            
        # Prepare columns and values for insertion
        columns = ", ".join(data.keys())
        placeholders = ", ".join([f"${i+1}" for i in range(len(data))])
        insert_query = f"INSERT INTO organization ({columns}) VALUES ({placeholders}) RETURNING *"
        params = list(data.values())
        
        result = execute_mutation(insert_query, params)
        if result:
            return {"status": "success", "data": result[0]}
        return {"status": "error", "message": "Failed to add organization to database."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def update_organization_db(org_id, data):
    set_clause = ", ".join([f"{key} = ${i+1}" for i, key in enumerate(data.keys())])
    query = f"UPDATE organization SET {set_clause} WHERE id = ${len(data)+1} RETURNING *"
    params = list(data.values()) + [org_id]
    
    result = execute_mutation(query, params)
    return result[0] if result else None


def delete_organization_db(org_id):
    # First, get the organization record to find the name and logo URL
    org_query = "SELECT organization, logo FROM organization WHERE id = $1"
    org_result = execute_query(org_query, (org_id,))
    if not org_result:
        # If organization doesn't exist, we can't proceed.
        raise Exception("Organization not found")

    org_data = org_result[0]
    organization_name = org_data.get("organization")
    logo_url = org_data.get("logo")

    # Handle associated ads using the organization name
    if organization_name:
        ads_query = "SELECT id, image FROM ads WHERE organization = $1"
        ads_result = execute_query(ads_query, (organization_name,))
        if ads_result:
            # Delete ad images from storage
            for ad in ads_result:
                if ad.get("image"):
                    delete_file_from_storage_by_url(ad.get("image"))
            # Delete ads from the database
            ad_ids = [ad['id'] for ad in ads_result]
            ad_ids_placeholders = ", ".join([f"${i+1}" for i in range(len(ad_ids))])
            delete_ads_query = f"DELETE FROM ads WHERE id IN ({ad_ids_placeholders})"
            execute_mutation(delete_ads_query, ad_ids)

    # Then, handle the organization's logo
    if logo_url:
        delete_file_from_storage_by_url(logo_url)

    # Finally, delete the organization record
    delete_org_query = "DELETE FROM organization WHERE id = $1 RETURNING *"
    result = execute_mutation(delete_org_query, (org_id,))
    return result


def get_ads_db():
    query = "SELECT * FROM ads ORDER BY created_at DESC"
    result = execute_query(query)
    return result if result else []


def add_ad_db(data):
    columns = ", ".join(data.keys())
    placeholders = ", ".join([f"${i+1}" for i in range(len(data))])
    query = f"INSERT INTO ads ({columns}) VALUES ({placeholders}) RETURNING *"
    params = list(data.values())
    
    result = execute_mutation(query, params)
    return result[0] if result else None


def update_ad_db(ad_id, data):
    set_clause = ", ".join([f"{key} = ${i+1}" for i, key in enumerate(data.keys())])
    query = f"UPDATE ads SET {set_clause} WHERE id = ${len(data)+1} RETURNING *"
    params = list(data.values()) + [ad_id]
    
    result = execute_mutation(query, params)
    return result[0] if result else None


def delete_ad_db(ad_id):
    # First, get the ad record to find the image URL
    ad_query = "SELECT image FROM ads WHERE id = $1"
    ad_result = execute_query(ad_query, (ad_id,))
    if ad_result and ad_result[0].get("image"):
        delete_file_from_storage_by_url(ad_result[0].get("image"))
        
    # Then, delete the ad record from the database
    delete_query = "DELETE FROM ads WHERE id = $1 RETURNING *"
    result = execute_mutation(delete_query, (ad_id,))
    return result


def get_orgs_db(org_id):
    query = "SELECT organization FROM organization WHERE id = $1"
    result = execute_query(query, (org_id,))
    return result[0] if result else None