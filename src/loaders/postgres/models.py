"""SQLAlchemy ORM models for Market Intelligence Hub PostgreSQL database."""

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Index, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""



class MarketQuoteORM(Base):
    """ORM representation of canonical MarketQuote schema."""

    __tablename__ = "market_quotes"
    __table_args__ = (
        UniqueConstraint(
            "ticker", "source", "ingested_at", name="uq_market_quote_ticker_source_dt"
        ),
        Index("idx_market_quote_ticker", "ticker"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    ticker: Mapped[str] = mapped_column(String(20), nullable=False)
    asset_class: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    current_price: Mapped[float | None] = mapped_column(nullable=True)
    market_cap: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    volume_24h: Mapped[float | None] = mapped_column(nullable=True)
    currency: Mapped[str] = mapped_column(String(10), default="USD", nullable=False)
    exchange: Mapped[str | None] = mapped_column(String(100), nullable=True)
    price_change_pct_24h: Mapped[float | None] = mapped_column(nullable=True)
    ingested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class FinancialArticleORM(Base):
    """ORM representation of canonical FinancialArticle schema."""

    __tablename__ = "financial_news"
    __table_args__ = (
        UniqueConstraint("url", name="uq_financial_news_url"),
        Index("idx_news_published_at", "published_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    author: Mapped[str | None] = mapped_column(String(255), nullable=True)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    content: Mapped[str | None] = mapped_column(nullable=True)
    source_name: Mapped[str] = mapped_column(String(255), nullable=False)
    source_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ingested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class PriceHistoryORM(Base):
    """ORM representation of canonical PriceBar schema."""

    __tablename__ = "price_bars"
    __table_args__ = (
        UniqueConstraint("ticker", "dt", name="uq_price_bar_ticker_dt"),
        Index("idx_price_bar_ticker_dt", "ticker", "dt"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    ticker: Mapped[str] = mapped_column(String(20), nullable=False)
    asset_class: Mapped[str] = mapped_column(String(50), nullable=False)
    dt: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    open: Mapped[float] = mapped_column(nullable=False)
    high: Mapped[float] = mapped_column(nullable=False)
    low: Mapped[float] = mapped_column(nullable=False)
    close: Mapped[float] = mapped_column(nullable=False)
    volume: Mapped[float] = mapped_column(nullable=False)
    ingested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
