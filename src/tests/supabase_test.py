from src.utils.supabase_client import get_supabase_client
supabase = get_supabase_client()

res = (
    supabase.table("orders")
    .select("*")
    .execute()
)
print(res)