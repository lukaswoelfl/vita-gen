from typing import List, Optional
from pydantic import BaseModel


class Experience(BaseModel):
    start_date: str
    end_date: str = "Heute"
    title: str
    company: str
    description: List[str]


class Education(BaseModel):
    start_date: str
    end_date: str
    degree: str
    institution: str
    details: List[str] = []


class SkillCategory(BaseModel):
    name: str
    skills: str


class Person(BaseModel):
    name: str
    title: str
    address: str
    phone: str
    email: str
    linkedin: str
    birth_date: str
    image_path: Optional[str] = None
    image_width: float = 32.0
    signature_path: Optional[str] = None
    signature_width: float = 40.0
    signature_date: Optional[str] = None


class CV(BaseModel):
    section_titles: Optional[dict] = None
    labels: Optional[dict] = None
    person: Person
    experiences: List[Experience]
    education: List[Education]
    skills: List[SkillCategory]
    languages: str
