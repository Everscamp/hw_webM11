from typing import List
from sqlalchemy import select
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact
from src.schemas import ContactBase, ContactResponse


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()
# async def get_contacts(limit: int, offset: int, db: AsyncSession):
#     stmt = select(Contact).offset(offset).limit(limit)
#     contacts = db.execute(stmt)

#     return contacts.scalars().all()


# async def get_contact(contact_id: int, db: Session) -> Contact:
#     return db.query(Contact).filter(Contact.id == contact_id).first()
async def get_contact(contact_id: int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    contact = db.execute(stmt)
    return contact.scalar_one_or_none()

async def get_contact_by_name(path, value: str, db: Session) -> Contact:
    if path == 'name':
        return db.query(Contact).filter(Contact.name == value).first()
    if path == 'surname':
        return db.query(Contact).filter(Contact.surname == value).first()
    if path == 'email':
        return db.query(Contact).filter(Contact.surname == value).first()
    
async def get_closest_birthdays(skip: int, limit: int, db: Session) -> List[Contact]:
    contacts = db.query(Contact).offset(skip).limit(limit).all()
    list_of_bees =[]
    for i in contacts:
        modified_date = i.birthday.replace(year=datetime.now().year + 1) \
        if i.birthday.month == 1 \
        else i.birthday.replace(year=datetime.now().year)
        result = modified_date - datetime.today()
        if result <= timedelta(days=7) and result >= timedelta(days=0):
            list_of_bees.append(i)

    return list_of_bees


async def create_contact(body: ContactBase, db: Session) -> Contact:
    contact = Contact(name=body.name, surname=body.surname, mobile=body.mobile, email=body.email, birthday=body.birthday)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactBase, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.name=body.name
        contact.surname=body.surname
        contact.mobile=body.mobile
        contact.email=body.email
        contact.birthday=body.birthday
        db.commit()
    return contact
