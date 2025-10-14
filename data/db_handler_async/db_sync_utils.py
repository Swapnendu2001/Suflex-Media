import asyncio
from typing import List, Dict, Any, Optional
from .db_pool import get_db_connection


def _run_async(async_func, *args, **kwargs):
    """Run an async function synchronously using the shared async runner."""
    from .sync_wrapper import run_async_function
    return run_async_function(async_func, *args, **kwargs)


def execute_query(query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
    """
    Execute a SELECT query and return results as list of dictionaries
    """
    async def _async_execute_query():
        async with get_db_connection() as conn:
            if params:
                rows = await conn.fetch(query, *params)
            else:
                rows = await conn.fetch(query)
            
            # Convert records to list of dictionaries
            return [dict(row) for row in rows]
    
    return _run_async(_async_execute_query)


def execute_mutation(query: str, params: Optional[tuple] = None) -> Optional[List[Dict[str, Any]]]:
    """
    Execute an INSERT, UPDATE, or DELETE query
    Returns the result if RETURNING clause is used, otherwise None
    """
    async def _async_execute_mutation():
        async with get_db_connection() as conn:
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
    
    return _run_async(_async_execute_mutation)


def execute_many(query: str, params_list: List[tuple]) -> None:
    """
    Execute a query multiple times with different parameters
    """
    async def _async_execute_many():
        async with get_db_connection() as conn:
            await conn.executemany(query, params_list)
    
    return _run_async(_async_execute_many)