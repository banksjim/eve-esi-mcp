from __future__ import annotations

from typing import Any

from ..esi_client import get_client
from ..sso import character_id, get_valid_access_token


async def _auth() -> tuple[str, int]:
    token = await get_valid_access_token()
    cid = await character_id()
    if not token or not cid:
        raise RuntimeError("Not logged in. Run sso_login first.")
    return token, cid


async def my_wallet() -> dict[str, Any]:
    """Wallet balance (requires esi-wallet.read_character_wallet.v1)."""
    token, cid = await _auth()
    balance = await get_client().get_json(
        f"/characters/{cid}/wallet/", auth_token=token
    )
    return {"character_id": cid, "balance_isk": balance}


async def my_wallet_journal() -> list[dict[str, Any]]:
    token, cid = await _auth()
    return await get_client().get_all_pages(
        f"/characters/{cid}/wallet/journal/", auth_token=token
    )


async def my_assets() -> list[dict[str, Any]]:
    """All assets the character owns (requires esi-assets.read_assets.v1)."""
    token, cid = await _auth()
    return await get_client().get_all_pages(
        f"/characters/{cid}/assets/", auth_token=token
    )


async def my_open_orders() -> list[dict[str, Any]]:
    """Open market orders (requires esi-markets.read_character_orders.v1)."""
    token, cid = await _auth()
    return await get_client().get_json(
        f"/characters/{cid}/orders/", auth_token=token
    )


async def my_wallet_transactions(
    from_id: int | None = None,
) -> list[dict[str, Any]]:
    """Individual market fills (requires esi-wallet.read_character_wallet.v1).

    Each entry: {transaction_id, date, type_id, quantity, unit_price, is_buy,
    is_personal, client_id, location_id, journal_ref_id}. Returns the most
    recent ~2500; pass `from_id` (a transaction_id) to page further back.

    This is the per-fill detail the wallet journal lacks — use it to reconcile
    buys against sells into round-trip trades.
    """
    token, cid = await _auth()
    params = {"from_id": from_id} if from_id is not None else None
    return await get_client().get_json(
        f"/characters/{cid}/wallet/transactions/",
        params=params,
        auth_token=token,
    )


async def my_order_history() -> list[dict[str, Any]]:
    """Closed market orders — filled, cancelled, or expired (requires
    esi-markets.read_character_orders.v1).

    Each entry carries `state` ("expired" covers both fully-filled and
    time-expired) plus `volume_total` vs `volume_remain`, which is how you tell
    a completed sale from an order that timed out unsold.
    """
    token, cid = await _auth()
    return await get_client().get_all_pages(
        f"/characters/{cid}/orders/history/", auth_token=token
    )


async def my_skills() -> dict[str, Any]:
    """Trained skills (requires esi-skills.read_skills.v1). Filter Accounting /
    Broker Relations / hauling skills to plug into arbitrage math."""
    token, cid = await _auth()
    return await get_client().get_json(
        f"/characters/{cid}/skills/", auth_token=token
    )


async def my_industry_jobs(include_completed: bool = False) -> list[dict[str, Any]]:
    """Industry jobs (requires esi-industry.read_character_jobs.v1)."""
    token, cid = await _auth()
    return await get_client().get_json(
        f"/characters/{cid}/industry/jobs/",
        params={"include_completed": str(include_completed).lower()},
        auth_token=token,
    )
