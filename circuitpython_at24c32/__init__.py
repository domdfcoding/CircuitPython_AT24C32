#!/usr/bin/env python3
#
#  __init__.py
"""
CircuitPython library to support AT24C39 EEPROM ICs.

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit's Bus Device library:
  https://github.com/adafruit/Adafruit_CircuitPython_BusDevice


**Notes:**

#. Datasheet: https://ww1.microchip.com/downloads/en/DeviceDoc/doc0336.pdf
"""
#
#  Copyright © 2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import time

# 3rd party
from adafruit_bus_device.i2c_device import I2CDevice  # type: ignore[import]

__author__ = "Dominic Davis-Foster"
__copyright__ = "2021 Dominic Davis-Foster"
__license__ = "MIT License"
__version__ = "0.0.0"
__email__ = "dominic@davis-foster.co.uk"
__repo__ = "https://github.com/domdfcoding/CircuitPython_AT24C32.git"

__all__ = ["AT24C32"]


class AT24C32:
	"""Interface to the AT24C32 EEPROM IC.

	**Quickstart: Importing and using the device**

		Here is an example of using the :class:`AT24C32` class.
		First you will need to import the required libraries:

		.. code-block:: python

			import board
			import at24c32

		Once this is done you can define your `board.I2C` object and create an `AT24C32` instance:

		.. code-block:: python

			i2c = board.I2C()  # uses board.SCL and board.SDA
			eeprom = at24c32.AT24C32(i2c)

		.. TODO:: Read and write data

	:param ~busio.I2C i2c: The I2C bus the device is connected to

	"""

	def __init__(self, i2c: I2CDevice, address: int = 0x50):
		self.i2c_device = I2CDevice(i2c, address)

	def write(
			self,
			val: "int | bytes | bytearray",
			start_addr: int,
			):
		"""
		Write ``val`` to the EEPROM, starting from ``start_addr``.

		* If ``val`` is an integer or a single byte, it is written to ``start_addr``.
		* If ``val`` is a :class:`bytearray` or a multi-byte string,
		  the bytes are written sequentially starting from ``start_addr``.

		`
		:param val: The value to write to the EEPROM.
		:param start_addr: The first address to write to.
		"""

		if isinstance(val, int):
			val = bytearray([val])

		with self.i2c_device:
			for offset, byte in enumerate(val):
				self.i2c_device.write(
						bytearray([
								((start_addr + offset) & 0b1111111100000000) >> 8,
								((start_addr + offset) & 0b11111111),
								byte,
								])
						)
				time.sleep(0.1)

	def read(self, start_addr: int, size: int = 1) -> bytearray:
		"""
		Read bytes from the EEPROM, starting from ``start_addr``.

		:param start_addr: The first address to start reading bytes from.
		:param size: The number of bytes to read. Bytes are read sequentially.
		"""

		buf = bytearray(size)

		with self.i2c_device:
			for offset in range(size):
				self.i2c_device.write(
						bytearray([
								(start_addr + offset & 0b1111111100000000) >> 8,
								(start_addr + offset & 0b11111111),
								])
						)
				time.sleep(0.1)
				self.i2c_device.readinto(buf, start=offset)

		return buf
