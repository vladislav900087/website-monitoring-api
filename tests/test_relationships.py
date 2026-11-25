from app.models.user import User
from app.models.website import Website
from app.models.check_result import CheckResult
from sqlalchemy.exc import IntegrityError
import pytest
from sqlalchemy import select


def test_user_website_relationship(db_session):

    user = User(email='test_user@example.com', hashed_password='hashed')

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user is not None

    first_website = Website(user_id=user.id, url='first_website_url', name='first_website')

    db_session.add(first_website)
    db_session.commit()
    db_session.refresh(first_website)

    assert first_website is not None
    assert first_website.user_id == user.id

    second_website = Website(user_id=user.id, url='second_website_url', name='second_website')

    db_session.add(second_website)
    db_session.commit()
    db_session.refresh(second_website)

    assert second_website is not None
    assert second_website.user_id == user.id

    assert len(user.websites) == 2
    assert user.websites[0] == first_website
    assert user.websites[1] == second_website

def test_website_user_url_unique_constraint(db_session):

    user = User(email='test_user@example.com', hashed_password='hashed')

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user is not None

    website = Website(user_id=user.id, url='website_url', name='website')

    db_session.add(website)
    db_session.commit()
    db_session.refresh(website)

    assert website is not None
    assert website.user_id == user.id

    with pytest.raises(IntegrityError):
        website = Website(user_id=user.id, url='website_url', name='website')

        db_session.add(website)
        db_session.commit()

    db_session.rollback()


def test_website_check_result_relationship(db_session):

    user = User(email='test_user@example.com', hashed_password='hashed')

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user is not None

    website = Website(user_id=user.id, url='website_url', name='website')

    db_session.add(website)
    db_session.commit()
    db_session.refresh(website)

    assert website is not None
    assert website.user_id == user.id

    first_check = CheckResult(website_id=website.id, status='UP', status_code=200, response_time_ms=100)

    db_session.add(first_check)
    db_session.commit()
    db_session.refresh(first_check)

    assert first_check is not None
    assert first_check.website_id == website.id

    second_check = CheckResult(website_id=website.id, status='DOWN', status_code=400, response_time_ms=100)

    db_session.add(second_check)
    db_session.commit()
    db_session.refresh(second_check)

    assert second_check is not None
    assert second_check.website_id == website.id

    assert len(website.checks) == 2
    assert website.checks[0] == first_check
    assert website.checks[1] == second_check

def test_delete_user_deletes_website(db_session):

    user = User(email='test_user@example.com', hashed_password='hashed')

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user is not None

    website = Website(user_id=user.id, url='website_url', name='website')

    db_session.add(website)
    db_session.commit()
    db_session.refresh(website)

    assert website is not None

    assert website.user_id == user.id

    db_session.delete(user)
    db_session.commit()

    statement = select(User).where(User.id == user.id)

    assert db_session.scalar(statement) is None

    statement = select(Website).where(Website.id == website.id)

    assert db_session.scalar(statement) is None

def test_delete_website_deletes_check(db_session):

    user = User(email='test_user@example.com', hashed_password='hashed')

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user is not None


    website = Website(user_id=user.id, url='website_url', name='website')

    db_session.add(website)
    db_session.commit()
    db_session.refresh(website)

    assert website is not None
    assert website.user_id == user.id

    check = CheckResult(website_id=website.id, status='UP', status_code=200, response_time_ms=100)

    db_session.add(check)
    db_session.commit()
    db_session.refresh(check)

    assert check is not None
    assert check.website_id == website.id

    db_session.delete(website)
    db_session.commit()

    statement = select(Website).where(Website.id == website.id)

    assert db_session.scalar(statement) is None

    statement = select(CheckResult).where(CheckResult.website_id == website.id)

    assert db_session.scalar(statement) is None

    statement = select(User).where(User.id == user.id)

    assert db_session.scalar(statement) is user




