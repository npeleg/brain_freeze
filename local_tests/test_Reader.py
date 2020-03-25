import .final
import pytest


def test_Reader():
	reader = asdF.Reader("./sample.mind.gz")
	assert reader.user.user_id == 42
	assert reader.user.username == "Dan Gittik"
	assert reader.user.birthday == 699746.4
	assert reader.user.gender.name == 'MALE'
	count_snapshots = 0
	for snapshot in reader:
		count_snapshots += 1
	assert count_snapshots == 367
