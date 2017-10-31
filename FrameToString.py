from PIL import Image
import pytesseract


class FrameToString:
    def __init__(self):
        self.stringDict = {}

    def process(self, plate):
        pil_plate = Image.fromarray(plate)
        tesser_string = pytesseract.image_to_string(pil_plate)
        if tesser_string == '': return
        candidate = ''
        lic_digit_counter = 0
        lic_char_counter = 0
        state_digit_counter = 0
        for char in tesser_string:
            if lic_digit_counter < 3 and char.isdigit():
                candidate += char
                lic_digit_counter += 1
            elif lic_char_counter < 3 and lic_digit_counter == 3:
                if char.isalpha():
                    candidate += char.capitalize()
                    lic_char_counter += 1
            elif state_digit_counter < 2 and (lic_char_counter == 2 or 3):
                if char.isdigit():
                    candidate += char
                    state_digit_counter += 1
        if not (lic_digit_counter == 3 and (lic_char_counter == 2 or 3) and state_digit_counter == 2):
            return
        self.stringDict[candidate] = self.stringDict[candidate] + 1 if self.stringDict.has_key(candidate) else 1
        return self.stringDict.keys()[self.stringDict.values().index(max(self.stringDict.values()))]