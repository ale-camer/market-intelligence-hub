"""Initial schema

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-08-28 20:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "001_initial_schema"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # market_quotes table
    op.create_table(
        "market_quotes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("source", sa.String(length=50), nullable=False),
        sa.Column("ticker", sa.String(length=20), nullable=False),
        sa.Column("asset_class", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("current_price", sa.Float(), nullable=True),
        sa.Column("market_cap", sa.BigInteger(), nullable=True),
        sa.Column("volume_24h", sa.Float(), nullable=True),
        sa.Column("currency", sa.String(length=10), nullable=False),
        sa.Column("exchange", sa.String(length=100), nullable=True),
        sa.Column("price_change_pct_24h", sa.Float(), nullable=True),
        sa.Column("ingested_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("ticker", "source", "ingested_at", name="uq_market_quote_ticker_source_dt"),
    )
    op.create_index("idx_market_quote_ticker", "market_quotes", ["ticker"])

    # financial_news table
    op.create_table(
        "financial_news",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("source", sa.String(length=50), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("description", sa.String(length=2048), nullable=True),
        sa.Column("url", sa.String(length=2048), nullable=False),
        sa.Column("image_url", sa.String(length=2048), nullable=True),
        sa.Column("author", sa.String(length=255), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("source_name", sa.String(length=255), nullable=False),
        sa.Column("source_id", sa.String(length=100), nullable=True),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.Column("ingested_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("url", name="uq_financial_news_url"),
    )
    op.create_index("idx_news_published_at", "financial_news", ["published_at"])

    # price_bars table
    op.create_table(
        "price_bars",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("source", sa.String(length=50), nullable=False),
        sa.Column("ticker", sa.String(length=20), nullable=False),
        sa.Column("asset_class", sa.String(length=50), nullable=False),
        sa.Column("dt", sa.DateTime(timezone=True), nullable=False),
        sa.Column("open", sa.Float(), nullable=False),
        sa.Column("high", sa.Float(), nullable=False),
        sa.Column("low", sa.Float(), nullable=False),
        sa.Column("close", sa.Float(), nullable=False),
        sa.Column("volume", sa.Float(), nullable=False),
        sa.Column("ingested_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("ticker", "dt", name="uq_price_bar_ticker_dt"),
    )
    op.create_index("idx_price_bar_ticker_dt", "price_bars", ["ticker", "dt"])


def downgrade() -> None:
    op.drop_table("price_bars")
    op.drop_table("financial_news")
    op.drop_table("market_quotes")
