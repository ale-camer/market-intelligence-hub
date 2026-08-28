"""Repository implementation for PostgreSQL storage using SQLAlchemy 2.0."""

from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.loaders.postgres.models import (
    Base,
    FinancialArticleORM,
    MarketQuoteORM,
    PriceHistoryORM,
)
from src.schemas.market import MarketQuote, PriceBar
from src.schemas.news import FinancialArticle


class PostgresRepository:
    """Repository pattern for handling PostgreSQL database operations."""

    def __init__(self, database_url: str = "sqlite:///:memory:") -> None:
        """Initialize database engine and sessionmaker."""
        self.engine = create_engine(database_url, echo=False)
        self.session_factory = sessionmaker(bind=self.engine, expire_on_commit=False)

    def create_tables(self) -> None:
        """Create all tables in database metadata."""
        Base.metadata.create_all(self.engine)

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Provide a transactional scope around a series of operations."""
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def upsert_market_quote(self, quote: MarketQuote) -> MarketQuoteORM:
        """Save a market quote into the database."""
        orm_obj = MarketQuoteORM(
            source=quote.source.value,
            ticker=quote.ticker,
            asset_class=quote.asset_class.value,
            name=quote.name,
            current_price=quote.current_price,
            market_cap=quote.market_cap,
            volume_24h=quote.volume_24h,
            currency=quote.currency,
            exchange=quote.exchange,
            price_change_pct_24h=quote.price_change_pct_24h,
            ingested_at=quote.ingested_at,
        )
        with self.get_session() as session:
            session.add(orm_obj)
        return orm_obj

    def bulk_insert_news(self, articles: list[FinancialArticle]) -> int:
        """Bulk insert news articles into database."""
        orm_objs = [
            FinancialArticleORM(
                source=article.source.value,
                title=article.title,
                description=article.description,
                url=article.url,
                image_url=article.image_url,
                author=article.author,
                published_at=article.published_at,
                content=article.content,
                source_name=article.source_name,
                source_id=article.source_id,
                category=article.category,
                ingested_at=article.ingested_at,
            )
            for article in articles
        ]
        with self.get_session() as session:
            session.add_all(orm_objs)
        return len(orm_objs)

    def bulk_insert_price_bars(self, bars: list[PriceBar]) -> int:
        """Bulk insert OHLCV price bars into database."""
        orm_objs = [
            PriceHistoryORM(
                source=bar.source.value,
                ticker=bar.ticker,
                asset_class=bar.asset_class.value,
                dt=bar.dt,
                open=bar.open,
                high=bar.high,
                low=bar.low,
                close=bar.close,
                volume=bar.volume,
                ingested_at=bar.ingested_at,
            )
            for bar in bars
        ]
        with self.get_session() as session:
            session.add_all(orm_objs)
        return len(orm_objs)
