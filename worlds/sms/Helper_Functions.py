class StringByteFunction:
    @staticmethod
    def string_to_bytes(user_string: str, encoded_byte_length: int) -> bytes:
        """
        Encodes a provided string to UTF-8 format. Adds padding until the expected length is reached.
        If provided string is longer than expected length, raise an exception

        :param user_string: String that needs to be encoded to bytes
        :param encoded_byte_length: Expected length of the provided string.
        """
        encoded_string = user_string.encode("utf-8")

        if len(encoded_string) < encoded_byte_length:
            encoded_string += b'\x00' * (encoded_byte_length - len(encoded_string))
        elif len(encoded_string) > encoded_byte_length:
            raise Exception(f"Provided string {user_string} was longer than the expected byte length of " +
                            f"{str(encoded_byte_length)}, which will not be accepted by the info file")
        
        return encoded_string