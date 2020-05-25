import gzip
import struct

SAMPLE_PATH = "./sample/sample.mind.gz"
OUTPUT_PATH = "./tests/utils/small_sample.mind.gz"
NUM_SNAPSHOTS = 5

with gzip.open(SAMPLE_PATH) as file:
    """ Create a small sample from the binary file, to use in non-local tests """
    seq = message_size = file.read(struct.calcsize('I'))
    user_size = struct.unpack('I', message_size)[0]
    seq += file.read(user_size)
    for i in range(NUM_SNAPSHOTS):
        message_size = file.read(struct.calcsize('I'))
        seq += message_size
        snapshot_size = struct.unpack('I', message_size)[0]
        seq += file.read(snapshot_size)

with gzip.open(OUTPUT_PATH, 'wb') as file:
    file.write(seq)
