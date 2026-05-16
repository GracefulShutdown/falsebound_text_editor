import re


class Falsebound_Text_Editor:
    """A versatile utility class for converting between custom 2-byte hex,
    literal ASCII, and shifted decoded text.
    """

    def to_hex_blocks(self, raw_input: str) -> str:
        """Takes raw text and generates the custom 2-byte hex blocks.
        Subtracts 0x20 from the standard ASCII value to encode.
        """
        hex_output = []
        last_index = len(raw_input) - 1

        for i, char in enumerate(raw_input):
            byte1 = "A0" if i == last_index else "00"
            byte2_val = ord(char) - 0x20

            if byte2_val < 0:
                byte2_val = 0

            byte2 = f"{byte2_val:02X}"
            hex_output.append(f"{byte1}{byte2}")

        return " ".join(hex_output)

    def _extract_byte2_list(self, hex_input: str) -> list:
        """Internal helper to clean up hex formatting and extract Byte 2 values."""
        hex_pairs = re.findall(r'[0-9a-fA-F]{2}', hex_input)
        byte2_values = []

        for i in range(0, len(hex_pairs), 2):
            if i + 1 < len(hex_pairs):
                byte1 = hex_pairs[i].upper()
                byte2 = hex_pairs[i + 1].upper()
            else:
                byte1 = "00"
                byte2 = hex_pairs[i].upper()

            byte2_values.append(int(byte2, 16))
            if byte1 == "A0":
                break

        return byte2_values

    def to_literal_ascii(self, hex_input: str) -> str:
        """Extracts Byte 2 as literal text with zero offset adjustment."""
        byte2_ints = self._extract_byte2_list(hex_input)
        chars = [chr(b) if 32 <= b <= 126 else "." for b in byte2_ints]
        return "".join(chars)

    def to_decoded_string(self, hex_input: str) -> str:
        """Applies the +0x20 offset calculation to return the true decoded text."""
        byte2_ints = self._extract_byte2_list(hex_input)
        # FIXED: Added + 0x20 instead of subtraction to perfectly restore the text
        chars = [chr(b + 0x20) if 32 <= (b + 0x20) <= 126 else "." for b in byte2_ints]
        return "".join(chars)


#Class tests in main
if __name__ == "__main__":
    #instance of the class
    fbk = Falsebound_Text_Editor()

    # ----------------------------------------------------
    # TEST 1: Plain Text -> Hex -> Literal ASCII (Your original test)
    # ----------------------------------------------------
    test_string = "Blue Medicine"
    hex_result = fbk.to_hex_blocks(test_string)

    print("=== TEST 1: Text Ingest ===")
    print(f"Input Text:       {test_string}")
    print(f"Encoded Hex:      {hex_result}")
    print(f"Hex Editor ASCII: {fbk.to_literal_ascii(hex_result)}\n")
    # ----------------------------------------------------
    # TEST 2: Testing Raw Hex Directly (Different formats)
    # ----------------------------------------------------
    print("=== TEST 2: Raw Hex Ingest ===")

    # Format A: Structured block formatting matching your tool's output style
    hex_blocks = "0022 004C 0055 0045 0000 002D 0045 0044 0049 0043 0049 004E A045"
    print(f"Input Hex Blocks: {hex_blocks}")
    print(f"Literal ASCII:    {fbk.to_literal_ascii(hex_blocks)}")
    print(f"Decoded String:   {fbk.to_decoded_string(hex_blocks)}\n")

    # Format B: Continuous stream without any spaces (like raw file contents)
    raw_stream = "0022004C005500450000002D00450044004900430049004EA045"
    print(f"Input Raw Stream: {raw_stream}")
    print(f"Literal ASCII:    {fbk.to_literal_ascii(raw_stream)}")
    print(f"Decoded String:   {fbk.to_decoded_string(raw_stream)}\n")

    # Format C: Individual standalone byte sequences (aa bb cc dd)
    byte_sequence = "00 22 00 4C 00 55 00 45 00 00 00 2D 00 45 00 44 00 49 00 43 00 49 00 4E A0 45"
    print(f"Input Bytes:      {byte_sequence}")
    print(f"Literal ASCII:    {fbk.to_literal_ascii(byte_sequence)}")
    print(f"Decoded String:   {fbk.to_decoded_string(byte_sequence)}\n")
