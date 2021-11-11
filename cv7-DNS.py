#!/usr/bin/env python
import struct

#DNS hlavicka
transaction_id = 0x1234
flags = 0x0100
question_count = 1
answer_count = 0
authority_count = 0
additional_count = 0
