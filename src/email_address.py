class EmailAddress:
    def __init__(self, raw_address: str):
        self._address = ""
        temp_address = self._normalize_address(raw_address)

        if self._check_correct_email(temp_address):
            self._address = temp_address
        else:
            raise ValueError(f"Некорректный email адрес: {raw_address}")

    @property
    def address(self) -> str:
        return self._address

    @property
    def masked(self) -> str:
        if not self._address:
            return ""
        try:
            name_part, domain_part = self._address.split('@', 1)
            prefix = name_part[:2]
            return f"{prefix}***@{domain_part}"
        except ValueError:
            return self._address

    def _normalize_address(self, raw_addr: str) -> str:
        if not raw_addr:
            return ""
        return raw_addr.strip().lower()

    def _check_correct_email(self, addr: str) -> bool:
        allowed_domains = ('.com', '.ru', '.net')
        return '@' in addr and addr.endswith(allowed_domains)

    def __str__(self):
        return self.masked

    def __repr__(self):
        return f"EmailAddress({self.address})"