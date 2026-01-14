from dataclasses import dataclass, field
from typing import List, Union, Optional
from src.status import Status
from src.email_address import EmailAddress
from src.utils import clean_text

@dataclass
class Email:
    subject: str
    body: str
    sender: EmailAddress
    recipients: Union[EmailAddress, List[EmailAddress]]
    date: Optional[str] = None
    short_body: Optional[str] = None
    status: Status = field(default=Status.DRAFT)

    def __post_init__(self):
        if isinstance(self.recipients, EmailAddress):
            self.recipients = [self.recipients]
        elif self.recipients is None:
            self.recipients = []

    def get_recipients_str(self) -> str:
        return ", ".join([r.masked for r in self.recipients])

    def clean_data(self) -> "Email":
        self.subject = clean_text(self.subject)
        self.body = clean_text(self.body)
        return self

    def add_short_body(self, n: int = 10) -> "Email":
        if not self.body:
            self.short_body = None  # Изменено с "" на None для тестов
        elif len(self.body) <= n:
            self.short_body = self.body
        else:
            self.short_body = self.body[:n] + "..."
        return self

    def is_valid_fields(self) -> bool:
        return bool(self.subject and self.body)

    def prepare(self) -> "Email":
        self.clean_data()
        self.add_short_body()

        has_content = self.is_valid_fields()
        has_sender = self.sender is not None
        has_recipients = isinstance(self.recipients, list) and len(self.recipients) > 0

        if has_content and has_sender and has_recipients:
            self.status = Status.READY
        else:
            self.status = Status.INVALID
        return self

    def __str__(self) -> str:
        recipients_str = self.get_recipients_str()
        content = self.short_body if self.short_body else self.body
        date_str = self.date if self.date else "не отправлено"
        return (
            f"Status: {self.status}\n"
            f"Кому: {recipients_str}\n"
            f"От: {self.sender.masked}\n"
            f"Тема: {self.subject}, дата {date_str}\n"
            f"{content}"
        )

    def __repr__(self) -> str:
        return self.__str__()