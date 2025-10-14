import asyncpg
from typing import List, Dict, Any, Optional
from .db_pool import get_db_connection


async def execute_query(query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
    """
    Execute a SELECT query and return results as list of dictionaries
    """
    conn_context = await get_db_connection()
    async with conn_context as conn:
        if params:
            rows = await conn.fetch(query, *params)
        else:
            rows = await conn.fetch(query)
        
        # Convert records to list of dictionaries
        return [dict(row) for row in rows]


async def execute_mutation(query: str, params: Optional[tuple] = None) -> Optional[List[Dict[str, Any]]]:
    """
    Execute an INSERT, UPDATE, or DELETE query
    Returns the result if RETURNING clause is used, otherwise None
    """
    conn_context = await get_db_connection()
    async with conn_context as conn:
        if params:
            if "RETURNING" in query.upper():
                rows = await conn.fetch(query, *params)
                return [dict(row) for row in rows]
            else:
                await conn.execute(query, *params)
                return None
        else:
            if "RETURNING" in query.upper():
                rows = await conn.fetch(query)
                return [dict(row) for row in rows]
            else:
                await conn.execute(query)
                return None


async def execute_many(query: str, params_list: List[tuple]) -> None:
    """
    Execute a query multiple times with different parameters
    """
    conn_context = await get_db_connection()
    async with conn_context as conn:
        await conn.executemany(query, params_list)