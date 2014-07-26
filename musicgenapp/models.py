import uuid
import hashlib
import random
import wave

from django.db import models
from django.core.files.storage import default_storage

from pydub import AudioSegment

# Create your models here.

class MusicGenUser(models.Model):

	email = models.EmailField(unique = True)
	passwordHash = models.CharField(max_length = 128)
	passwordSalt = models.CharField(max_length = 32)
	resetCode = models.CharField(max_length = 32, null = True, blank = True, default = "")

	def setPassword(self, password):
		# Generate random salt
		salt = uuid.uuid4().hex
		# Apply salt to password
		pSalted = password + salt
		# Hash the salted password
		pHashed = hashlib.sha512(pSalted).hexdigest()
		# Store the results for later
		self.passwordHash = pHashed
		self.passwordSalt = salt

	def checkPassword(self, password):
		# Apply salt to password
		pSalted = password + self.passwordSalt
		# Hash the salted password
		pHashed = hashlib.sha512(pSalted).hexdigest()
		# Check it against the stored one
		return self.passwordHash == pHashed

class SongWrapper(models.Model):

	active = models.BooleanField(default = True)
	latest = models.ForeignKey('Song', null = True, blank = True)
	generation = models.IntegerField(default = 1)

class Song(models.Model):

	# Comma-separated ints
	pitches = models.CharField(max_length = 64)
	# 1 = whole note, 2 = half note, 4 = quarter note, 8 = eighth note
	durations = models.CharField(max_length = 64)
	# Which generation are we on? starting at 1
	generation = models.IntegerField(default = 1)
	# How many ratings have we received in this generation?
	numRatings = models.IntegerField(default = 0)
	# Average rating in this generation
	avgRating = models.IntegerField(default = 0)
	# Use wrapper to keep track of previous generations
	# New generation creates new song object
	wrapper = models.ForeignKey('SongWrapper')
	# Is this the latest generation for this wrapper?
	latest = models.BooleanField(default = True)
	# Actual song file
	wav = models.FileField(upload_to = 'songs', null = True, blank = True)

	@classmethod
	def random(cls, wrapper):

		pitches = []
		durations = []
		# 8 / each duration
		inverseDurations = []

		# 8 beats per measure, 4 measures
		while sum(inverseDurations) < 8 * 4:
			# Just put in random pitches
			pitches.append(random.randint(0, 24))
			remaining = 8 * 4 - sum(inverseDurations)
			possibleInverseDurations = {8, 4, 2, 1}
			# Don't go over 4 measures
			# TODO: optimize?
			if remaining < 2:
				possibleInverseDurations.remove(8)
				possibleInverseDurations.remove(4)
				possibleInverseDurations.remove(2)
			elif remaining < 4:
				possibleInverseDurations.remove(8)
				possibleInverseDurations.remove(4)
			elif remaining < 8:
				possibleInverseDurations.remove(8)
			inverseDuration = random.choice(tuple(possibleInverseDurations))
			inverseDurations.append(inverseDuration)
			durations.append(8 / inverseDuration)

		obj = cls(pitches = ','.join(map(str, pitches)), durations = ','.join(map(str, durations)), wrapper = wrapper)
		# Probably bad practice to save here instead of just returning it but whatever... I need the pk in order to make the file
		obj.save()

		# Finished generating attributes, now generate actual file
		wav = default_storage.open('songs/' + str(obj.pk) + '.wav', 'wb')

		pitchTable = {
			0: 'C3',
			1: 'Cs3',
			2: 'D3',
			3: 'Ds3',
			4: 'E3',
			5: 'F3',
			6: 'Fs3',
			7: 'G3',
			8: 'Gs3',
			9: 'A3',
			10: 'As3',
			11: 'B3',
			12: 'C4',
			13: 'Cs4',
			14: 'D4',
			15: 'Ds4',
			16: 'E4',
			17: 'F4',
			18: 'Fs4',
			19: 'G4',
			20: 'Gs4',
			21: 'A4',
			22: 'As4',
			23: 'B4',
			24: 'C5'
		}

		durationTable = {
			1: 2400,
			2: 1200,
			4: 600,
			8: 300
		}

		final = None

		for pitch, duration in zip(pitches, durations):
			fn = 'pitches/' + pitchTable[pitch] + '.wav'
			pf = default_storage.open(fn)
			if final is None:
				final = AudioSegment(pf)[0:durationTable[duration]]
			else:
				final += AudioSegment(pf)[0:durationTable[duration]]

		# Copied from AudioSegment source...
		# I should have changed AudioSegment (getWaveFileContents() or something) and submitted a pull request but I have a deadline
		wave_data = wave.open(wav)
		wave_data.setnchannels(self.channels)
		wave_data.setsampwidth(self.sample_width)
		wave_data.setframerate(self.frame_rate)
		wave_data.setnframes(int(self.frame_count()))
		wave_data.writeframesraw(self._data)
		wave_data.close()

		wav.close()

		return obj

class Rating(models.Model):

	song = models.ForeignKey('Song')
	user = models.ForeignKey('MusicGenUser')
	generation = models.IntegerField()
	value = models.IntegerField()