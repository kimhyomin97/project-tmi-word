"""
정제된 CSV를 PostgreSQL에 적재하는 스크립트 (자체 완결형)

FastAPI 앱(app/)과 독립적으로 동작합니다.
DB 조회는 Spring Boot에서 수행하므로, 이 스크립트는 적재 전용입니다.

사전 조건:
  1. PostgreSQL 실행 중
  2. DB 생성 완료: CREATE DATABASE tmi_word;
  3. pip install sqlalchemy psycopg2-binary

실행:
  python scripts/load_data.py
"""

import csv
import enum
import os
import sys
import time
from pathlib import Path

from sqlalchemy import (
    create_engine, Column, Integer, String, Text, Enum, Index, func
)
from sqlalchemy.orm import sessionmaker, declarative_base

# ──────────────────────────────────────────────
# DB 설정
# ──────────────────────────────────────────────
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/tmi_word"
)

engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# ──────────────────────────────────────────────
# ORM 모델 (적재 전용 — Spring Boot JPA Entity와 동일 구조)
# ──────────────────────────────────────────────
class Difficulty(str, enum.Enum):
    STARTER = "STARTER"
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    CHALLENGE = "CHALLENGE"


class Sentence(Base):
    __tablename__ = "sentences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    english_text = Column(Text, nullable=False)
    korean_ref = Column(Text, nullable=False)
    difficulty = Column(
        Enum(Difficulty, name="difficulty_level", create_type=True),
        nullable=False,
    )
    category = Column(String(50), nullable=False, default="DAILY")
    subcategory = Column(String(100), nullable=False, default="")
    source = Column(String(30), nullable=False)

    __table_args__ = (
        Index("ix_sentences_diff_cat", "difficulty", "category"),
    )


# ──────────────────────────────────────────────
# 적재 로직
# ──────────────────────────────────────────────
CSV_PATH = Path(__file__).parent / "cleansed_sentences.csv"
BATCH_SIZE = 5000


def create_tables():
    Base.metadata.create_all(engine)
    print("테이블 생성 완료")


def load_csv():
    if not CSV_PATH.exists():
        print(f"CSV 파일 없음: {CSV_PATH}")
        print("먼저 python scripts/cleanse_data.py 를 실행하세요.")
        sys.exit(1)

    session = Session()

    deleted = session.query(Sentence).delete()
    session.commit()
    if deleted > 0:
        print(f"기존 데이터 {deleted:,}건 삭제")

    start = time.time()
    total = 0
    batch = []

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            batch.append(Sentence(
                english_text=row["english_text"],
                korean_ref=row["korean_ref"],
                difficulty=Difficulty(row["difficulty"]),
                category=row["category"],
                subcategory=row["subcategory"],
                source=row["source"],
            ))
            if len(batch) >= BATCH_SIZE:
                session.bulk_save_objects(batch)
                session.commit()
                total += len(batch)
                elapsed = time.time() - start
                rate = total / elapsed if elapsed > 0 else 0
                print(f"  {total:>8,}건 적재 ({rate:,.0f}건/초)")
                batch = []

    if batch:
        session.bulk_save_objects(batch)
        session.commit()
        total += len(batch)

    elapsed = time.time() - start
    session.close()
    print(f"\n적재 완료: {total:,}건 ({elapsed:.1f}초)")
    return total


def print_stats():
    session = Session()
    total = session.query(Sentence).count()
    print(f"\n총 문장 수: {total:,}")

    print("\n난이도별:")
    for diff in Difficulty:
        count = session.query(Sentence).filter(Sentence.difficulty == diff).count()
        pct = count / max(total, 1) * 100
        print(f"  {diff.value:15s}: {count:>8,}  ({pct:5.1f}%)")

    print("\n카테고리별:")
    cats = (
        session.query(Sentence.category, func.count())
        .group_by(Sentence.category)
        .order_by(func.count().desc())
        .all()
    )
    for cat, count in cats:
        pct = count / max(total, 1) * 100
        print(f"  {cat:15s}: {count:>8,}  ({pct:5.1f}%)")

    session.close()


def main():
    print("=" * 50)
    print("CSV → PostgreSQL 적재")
    print("=" * 50)
    create_tables()
    load_csv()
    print_stats()
    print("\n완료!")


if __name__ == "__main__":
    main()
