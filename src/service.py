from datetime import datetime
from typing import List
from src.email import Email
from src.status import Status

class EmailService:
    def __init__(self, email: Email):
        self.email = email

    def _get_current_date(self) -> str:
        return datetime.now().strftime("%Y-%m-%d")

    def send_email(self) -> List[Email]:
        sent_emails = []
        current_date = self._get_current_date()

        for recipient in self.email.recipients:
            # Создаем новый объект, но передаем существующие ссылки на объекты адресов
            email_copy = Email(
                subject=self.email.subject,
                body=self.email.body,
                sender=self.email.sender,
                recipients=[recipient],
                date=current_date,
                short_body=self.email.short_body
            )

            if self.email.status == Status.READY:
                email_copy.status = Status.SENT
            else:
                email_copy.status = Status.FAILED

            sent_emails.append(email_copy)

        return sent_emails

class LoggingEmailService(EmailService):
    def __init__(self, email: Email, log_file: str = "send.log"):
        super().__init__(email)
        self.log_file = log_file

    def send_email(self) -> List[Email]:
        results = super().send_email()
        self._log_results(results)
        return results

    def _log_results(self, emails: List[Email]):
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                for mail in emails:
                    log_entry = (
                        f"[{datetime.now()}] Sent to: {mail.get_recipients_str()} | "
                        f"Status: {mail.status} | Subject: {mail.subject}\n"
                    )
                    f.write(log_entry)
        except IOError as e:
            print(f"Ошибка записи лога: {e}")