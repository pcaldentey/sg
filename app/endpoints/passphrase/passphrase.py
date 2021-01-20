class PassphraseResource:
    def __init__(self, request):
        self.passphrases = request.json['passphrase'].split('\n')
        self.passphrases_total = len(self.passphrases)

    def _has_repeated_elements(self, pphrase: list):
        return len(pphrase) != len(set(pphrase))

    def _has_anagrams(self, pphrase: list):
        # set of elements of pphrase list, each element is sorted alphabetically
        sorted_strings_set = {"".join(sorted(s)) for s in pphrase}
        return len(pphrase) != len(sorted_strings_set)

    def basic(self):
        valid_pp = 0
        for phrase in self.passphrases:
            if not self._has_repeated_elements(phrase.split(' ')):
                valid_pp += 1

        return {'total passphrases': self.passphrases_total, "valid passphrases": valid_pp}

    def advanced(self):
        valid_pp = 0
        for phrase in self.passphrases:
            if not self._has_anagrams(phrase.split(' ')):
                valid_pp += 1

        return {'total passphrases': self.passphrases_total, "valid passphrases": valid_pp}
