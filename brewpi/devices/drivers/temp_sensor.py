# If we aren't on an RPi, this module still provides dummy data for testing.

try:
    import RPi.GPIO as GPIO
    import spidev

    class TempSensorDriver:
        REG_CONFIG = 0x00
        REG_RTD_MSB = 0x01
        REG_RTD_LSB = 0x02
        REG_HIFLT_MSB = 0x03
        REG_HIFLT_LSB = 0x04
        REG_LOFLT_MSB = 0x05
        REG_LOFLT_LSB = 0x06
        REG_FLT_STATUS = 0x07

        WRITE_FLAG = 0x80

        RREF = 430  # reference resistor in Ohms
        CONFIG = 0xD1

        def setup(gpio, activeLow):
            if gpio:
                GPIO.setwarnings(False)
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(gpio, GPIO.OUT)
                TempSensorDriver.chip_select(False, gpio, activeLow)

            TempSensorDriver.write_spi(
                gpio, TempSensorDriver.REG_CONFIG, [TempSensorDriver.CONFIG], activeLow
            )  # set up device
            r = TempSensorDriver.read_spi(
                gpio, TempSensorDriver.REG_CONFIG, 1, activeLow
            )[
                0
            ]  # read config back
            if r != TempSensorDriver.CONFIG:
                print("Error setting config")

        def chip_select(select, gpio, activeLow):
            if gpio:  # 0 or none, rely on normal SPI CS
                if select == activeLow:
                    en = GPIO.LOW
                else:
                    en = GPIO.HIGH
                GPIO.output(gpio, en)  # enable

        def read_spi(gpio, reg, length, activeLow):
            rtd = spidev.SpiDev()
            rtd.open(0, 0)
            rtd.max_speed_hz = 5000
            rtd.mode = 1
            d = [0] * (length + 1)
            d[0] = reg
            TempSensorDriver.chip_select(True, gpio, activeLow)
            r = rtd.xfer2(d)
            TempSensorDriver.chip_select(False, gpio, activeLow)
            rtd.close()
            return r[1:]

        def write_spi(gpio, reg, data, activeLow):
            rtd = spidev.SpiDev()
            rtd.open(0, 0)
            rtd.max_speed_hz = 5000
            rtd.mode = 1
            d = list()
            d.append(reg + TempSensorDriver.WRITE_FLAG)
            d.extend(data)
            TempSensorDriver.chip_select(True, gpio, activeLow)
            r = rtd.xfer2(d)
            TempSensorDriver.chip_select(False, gpio, activeLow)
            rtd.close()
            return

        def getTemp_degc(gpio, activeLow=True):
            TempSensorDriver.setup(gpio, activeLow)
            r = TempSensorDriver.read_spi(
                gpio, TempSensorDriver.REG_RTD_MSB, 2, activeLow
            )
            rtdval = r[0] * 256 + r[1]
            if (rtdval % 2) == 1:  # lowest bit is a fault flag
                r = TempSensorDriver.read_spi(
                    gpio, TempSensorDriver.REG_FLT_STATUS, 1, activeLow
                )[0]
                print("Error 0x{:02x} detected".format(r))
                TempSensorDriver.write_spi(
                    gpio,
                    TempSensorDriver.REG_CONFIG,
                    [TempSensorDriver.CONFIG + 2],
                    activeLow,
                )  # try clear fault
                return None  # if fault is cleared, should read okay next time.
            rtdval = rtdval / 2
            rtdval = float(rtdval) * float(TempSensorDriver.RREF) / 32768.0
            temp = pt100.interp_resist_to_temp(rtdval)
            return temp


except:
    import math
    from datetime import datetime

    class TempSensorDriver:
        def getTemp_degc(gpio, activeLow=True):
            max = 100
            n = datetime.now().time()
            seconds = float(n.second) + float(n.microsecond) / 1000000.0
            return (math.sin(seconds * 2 * math.pi / 60 / (gpio + 1)) + 1) * max / 2


class pt100:

    temperature_vals = list(range(-200, 850 + 1))
    resistance_vals = [  # 18.52 Ohm correspond to a temperature of -200 deg C
        18.52,
        18.96,
        19.39,
        19.82,
        20.25,
        20.68,
        21.11,
        21.54,
        21.97,
        22.40,
        22.83,
        23.26,
        23.69,
        24.12,
        24.55,
        24.97,
        25.39,
        25.82,
        26.25,
        26.67,
        27.10,
        27.52,
        27.95,
        28.37,
        28.80,
        29.22,
        29.65,
        30.07,
        30.49,
        30.92,
        31.34,
        31.76,
        32.18,
        32.61,
        33.03,
        33.45,
        33.86,
        34.28,
        34.70,
        35.12,
        35.54,
        35.96,
        36.38,
        36.80,
        37.22,
        37.63,
        38.05,
        38.47,
        38.89,
        39.31,
        39.72,
        40.14,
        40.56,
        40.97,
        41.39,
        41.80,
        42.22,
        42.64,
        43.05,
        43.46,
        43.88,
        44.29,
        44.71,
        45.12,
        45.53,
        45.95,
        46.35,
        46.76,
        47.18,
        47.59,
        48.00,
        48.41,
        48.82,
        49.23,
        49.64,
        50.06,
        50.47,
        50.88,
        51.29,
        51.70,
        52.11,
        52.52,
        52.92,
        53.33,
        53.74,
        54.15,
        54.56,
        54.97,
        55.38,
        55.78,
        56.19,
        56.60,
        57.00,
        57.41,
        57.82,
        58.22,
        58.63,
        59.04,
        59.44,
        59.85,
        60.26,
        60.67,
        61.07,
        61.48,
        61.87,
        62.29,
        62.69,
        63.10,
        63.50,
        63.91,
        64.30,
        64.70,
        65.11,
        65.51,
        65.91,
        66.31,
        66.72,
        67.12,
        67.52,
        67.92,
        68.33,
        68.73,
        69.13,
        69.53,
        69.93,
        70.33,
        70.73,
        71.13,
        71.53,
        71.93,
        72.33,
        72.73,
        73.13,
        73.53,
        73.93,
        74.33,
        74.73,
        75.13,
        75.53,
        75.93,
        76.33,
        76.73,
        77.13,
        77.52,
        77.92,
        78.32,
        78.72,
        79.11,
        79.51,
        79.91,
        80.31,
        80.70,
        81.10,
        81.50,
        81.89,
        82.29,
        82.69,
        83.08,
        83.48,
        83.88,
        84.27,
        84.67,
        85.06,
        85.46,
        85.85,
        86.25,
        86.64,
        87.04,
        87.43,
        87.83,
        88.22,
        88.62,
        89.01,
        89.40,
        89.80,
        90.19,
        90.59,
        90.98,
        91.37,
        91.77,
        92.16,
        92.55,
        92.95,
        93.34,
        93.73,
        94.12,
        94.52,
        94.91,
        95.30,
        95.69,
        96.09,
        96.48,
        96.87,
        97.26,
        97.65,
        98.04,
        98.44,
        98.83,
        99.22,
        99.61,
        100.00,
        100.39,
        100.78,
        101.17,
        101.56,
        101.95,
        102.34,
        102.73,
        103.12,
        103.51,
        103.90,
        104.29,
        104.68,
        105.07,
        105.46,
        105.85,
        106.24,
        106.63,
        107.02,
        107.40,
        107.79,
        108.18,
        108.57,
        108.96,
        109.35,
        109.73,
        110.12,
        110.51,
        110.90,
        111.28,
        111.67,
        112.06,
        112.45,
        112.83,
        113.22,
        113.61,
        113.99,
        114.38,
        114.77,
        115.15,
        115.54,
        115.93,
        116.31,
        116.70,
        117.08,
        117.47,
        117.85,
        118.24,
        118.62,
        119.01,
        119.40,
        119.78,
        120.16,
        120.55,
        120.93,
        121.32,
        121.70,
        122.09,
        122.47,
        122.86,
        123.24,
        123.62,
        124.01,
        124.39,
        124.77,
        125.17,
        125.55,
        125.93,
        126.32,
        126.70,
        127.08,
        127.46,
        127.85,
        128.23,
        128.61,
        128.99,
        129.38,
        129.76,
        130.14,
        130.52,
        130.90,
        131.28,
        131.67,
        132.05,
        132.43,
        132.81,
        133.19,
        133.57,
        133.95,
        134.33,
        134.71,
        135.09,
        135.47,
        135.85,
        136.23,
        136.61,
        136.99,
        137.37,
        137.75,
        138.13,
        138.51,
        138.89,
        139.27,
        139.65,
        140.03,
        140.39,
        140.77,
        141.15,
        141.53,
        141.91,
        142.29,
        142.66,
        143.04,
        143.42,
        143.80,
        144.18,
        144.56,
        144.94,
        145.32,
        145.69,
        146.07,
        146.45,
        146.82,
        147.20,
        147.58,
        147.95,
        148.33,
        148.71,
        149.08,
        149.46,
        149.83,
        150.21,
        150.58,
        150.96,
        151.34,
        151.71,
        152.09,
        152.46,
        152.84,
        153.21,
        153.58,
        153.95,
        154.32,
        154.71,
        155.08,
        155.46,
        155.83,
        156.21,
        156.58,
        156.96,
        157.33,
        157.71,
        158.08,
        158.45,
        158.83,
        159.20,
        159.56,
        159.94,
        160.31,
        160.68,
        161.05,
        161.43,
        161.80,
        162.17,
        162.54,
        162.91,
        163.28,
        163.66,
        164.03,
        164.40,
        164.77,
        165.14,
        165.51,
        165.88,
        166.25,
        166.62,
        167.00,
        167.37,
        167.74,
        168.11,
        168.48,
        168.85,
        169.22,
        169.59,
        169.96,
        170.33,
        170.69,
        171.06,
        171.43,
        171.80,
        172.17,
        172.54,
        172.91,
        173.27,
        173.64,
        174.01,
        174.39,
        174.75,
        175.12,
        175.49,
        175.86,
        176.23,
        176.59,
        176.96,
        177.33,
        177.70,
        178.06,
        178.43,
        178.80,
        179.16,
        179.53,
        179.90,
        180.26,
        180.63,
        180.99,
        181.36,
        181.73,
        182.09,
        182.46,
        182.82,
        183.19,
        183.55,
        183.92,
        184.28,
        184.65,
        185.01,
        185.38,
        185.74,
        186.11,
        186.47,
        186.84,
        187.20,
        187.56,
        187.93,
        188.29,
        188.65,
        189.02,
        189.38,
        189.74,
        190.11,
        190.47,
        190.83,
        191.20,
        191.56,
        191.92,
        192.28,
        192.66,
        193.02,
        193.38,
        193.74,
        194.10,
        194.47,
        194.83,
        195.19,
        195.55,
        195.90,
        196.26,
        196.62,
        196.98,
        197.35,
        197.71,
        198.07,
        198.43,
        198.79,
        199.15,
        199.51,
        199.87,
        200.23,
        200.59,
        200.95,
        201.31,
        201.67,
        202.03,
        202.38,
        202.74,
        203.10,
        203.46,
        203.82,
        204.18,
        204.54,
        204.90,
        205.25,
        205.61,
        205.97,
        206.33,
        206.70,
        207.05,
        207.41,
        207.77,
        208.13,
        208.48,
        208.84,
        209.20,
        209.55,
        209.91,
        210.27,
        210.62,
        210.98,
        211.34,
        211.69,
        212.05,
        212.40,
        212.76,
        213.12,
        213.47,
        213.83,
        214.19,
        214.55,
        214.90,
        215.26,
        215.61,
        215.97,
        216.32,
        216.68,
        217.03,
        217.39,
        217.73,
        218.08,
        218.44,
        218.79,
        219.15,
        219.50,
        219.85,
        220.21,
        220.56,
        220.91,
        221.27,
        221.62,
        221.97,
        222.32,
        222.68,
        223.03,
        223.38,
        223.73,
        224.09,
        224.45,
        224.80,
        225.15,
        225.50,
        225.85,
        226.21,
        226.56,
        226.91,
        227.26,
        227.61,
        227.96,
        228.31,
        228.66,
        229.01,
        229.36,
        229.72,
        230.07,
        230.42,
        230.77,
        231.12,
        231.47,
        231.81,
        232.16,
        232.51,
        232.86,
        233.21,
        233.56,
        233.91,
        234.26,
        234.60,
        234.95,
        235.30,
        235.65,
        236.00,
        236.35,
        236.70,
        237.05,
        237.40,
        237.75,
        238.09,
        238.44,
        238.79,
        239.14,
        239.48,
        239.83,
        240.18,
        240.52,
        240.87,
        241.22,
        241.56,
        241.91,
        242.25,
        242.60,
        242.95,
        243.29,
        243.64,
        243.98,
        244.33,
        244.67,
        245.02,
        245.36,
        245.71,
        246.05,
        246.40,
        246.74,
        247.09,
        247.43,
        247.78,
        248.12,
        248.46,
        248.81,
        249.15,
        249.50,
        249.84,
        250.18,
        250.53,
        250.89,
        251.21,
        251.55,
        251.90,
        252.24,
        252.59,
        252.94,
        253.28,
        253.62,
        253.96,
        254.30,
        254.65,
        254.99,
        255.33,
        255.67,
        256.01,
        256.35,
        256.70,
        257.04,
        257.38,
        257.72,
        258.06,
        258.40,
        258.74,
        259.08,
        259.42,
        259.76,
        260.10,
        260.44,
        260.78,
        261.12,
        261.46,
        261.80,
        262.14,
        262.48,
        262.83,
        263.17,
        263.50,
        263.84,
        264.18,
        264.52,
        264.86,
        265.20,
        265.54,
        265.87,
        266.21,
        266.55,
        266.89,
        267.22,
        267.56,
        267.90,
        268.24,
        268.57,
        268.91,
        269.25,
        269.58,
        269.92,
        270.26,
        270.59,
        270.93,
        271.27,
        271.60,
        271.94,
        272.27,
        272.61,
        272.95,
        273.28,
        273.62,
        273.95,
        274.29,
        274.62,
        274.96,
        275.29,
        275.63,
        275.96,
        276.31,
        276.64,
        276.97,
        277.31,
        277.64,
        277.98,
        278.31,
        278.64,
        278.98,
        279.31,
        279.64,
        279.98,
        280.31,
        280.64,
        280.98,
        281.31,
        281.64,
        281.97,
        282.31,
        282.64,
        282.97,
        283.30,
        283.63,
        283.97,
        284.30,
        284.63,
        284.96,
        285.29,
        285.62,
        285.95,
        286.30,
        286.63,
        286.96,
        287.29,
        287.62,
        287.95,
        288.28,
        288.61,
        288.94,
        289.27,
        289.60,
        289.93,
        290.26,
        290.59,
        290.92,
        291.25,
        291.58,
        291.90,
        292.23,
        292.56,
        292.90,
        293.23,
        293.56,
        293.89,
        294.21,
        294.54,
        294.87,
        295.20,
        295.53,
        295.85,
        296.18,
        296.51,
        296.84,
        297.16,
        297.49,
        297.82,
        298.14,
        298.47,
        298.80,
        299.12,
        299.45,
        299.78,
        300.10,
        300.43,
        300.75,
        301.08,
        301.41,
        301.73,
        302.06,
        302.38,
        302.71,
        303.03,
        303.36,
        303.68,
        304.01,
        304.33,
        304.66,
        304.98,
        305.30,
        305.63,
        305.95,
        306.28,
        306.60,
        306.92,
        307.25,
        307.57,
        307.89,
        308.22,
        308.54,
        308.86,
        309.19,
        309.51,
        309.83,
        310.15,
        310.48,
        310.80,
        311.12,
        311.45,
        311.78,
        312.10,
        312.43,
        312.75,
        313.07,
        313.39,
        313.71,
        314.04,
        314.36,
        314.68,
        315.00,
        315.32,
        315.64,
        315.96,
        316.28,
        316.60,
        316.92,
        317.24,
        317.56,
        317.88,
        318.20,
        318.52,
        318.85,
        319.17,
        319.49,
        319.81,
        320.12,
        320.44,
        320.76,
        321.08,
        321.40,
        321.72,
        322.03,
        322.34,
        322.66,
        322.98,
        323.30,
        323.61,
        323.93,
        324.25,
        324.57,
        324.88,
        325.21,
        325.53,
        325.85,
        326.16,
        326.48,
        326.79,
        327.11,
        327.43,
        327.74,
        328.06,
        328.38,
        328.69,
        329.01,
        329.32,
        329.64,
        329.95,
        330.27,
        330.58,
        330.90,
        331.21,
        331.53,
        331.84,
        332.16,
        332.47,
        332.79,
        333.10,
        333.41,
        333.73,
        334.04,
        334.36,
        334.68,
        334.99,
        335.31,
        335.62,
        335.93,
        336.25,
        336.56,
        336.87,
        337.18,
        337.50,
        337.81,
        338.12,
        338.43,
        338.75,
        339.06,
        339.37,
        339.68,
        339.99,
        340.30,
        340.62,
        340.94,
        341.25,
        341.55,
        341.87,
        342.18,
        342.49,
        342.80,
        343.11,
        343.42,
        343.73,
        344.04,
        344.35,
        344.66,
        344.97,
        345.28,
        345.59,
        345.90,
        346.21,
        346.52,
        346.83,
        347.15,
        347.46,
        347.76,
        348.07,
        348.38,
        348.69,
        349.00,
        349.31,
        349.61,
        349.92,
        350.23,
        350.54,
        350.85,
        351.15,
        351.46,
        351.77,
        352.07,
        352.38,
        352.69,
        352.99,
        353.30,
        353.61,
        353.91,
        354.22,
        354.53,
        354.83,
        355.14,
        355.44,
        355.75,
        356.06,
        356.37,
        356.68,
        356.98,
        357.29,
        357.59,
        357.90,
        358.20,
        358.51,
        358.81,
        359.12,
        359.42,
        359.72,
        360.03,
        360.33,
        360.64,
        360.94,
        361.24,
        361.55,
        361.85,
        362.15,
        362.46,
        362.76,
        363.06,
        363.36,
        363.67,
        363.97,
        364.27,
        364.57,
        364.88,
        365.18,
        365.49,
        365.79,
        366.09,
        366.40,
        366.70,
        367.00,
        367.30,
        367.60,
        367.90,
        368.20,
        368.50,
        368.81,
        369.11,
        369.41,
        369.71,
        370.01,
        370.31,
        370.61,
        370.91,
        371.21,
        371.52,
        371.82,
        372.12,
        372.41,
        372.71,
        373.01,
        373.31,
        373.61,
        373.91,
        374.21,
        374.51,
        374.80,
        375.10,
        375.40,
        375.70,
        376.00,
        376.29,
        376.59,
        376.89,
        377.19,
        377.49,
        377.79,
        378.09,
        378.39,
        378.68,
        378.98,
        379.28,
        379.57,
        379.87,
        380.17,
        380.46,
        380.76,
        381.05,
        381.35,
        381.65,
        381.94,
        382.24,
        382.53,
        382.83,
        383.12,
        383.42,
        383.71,
        384.01,
        384.30,
        384.60,
        384.89,
        385.18,
        385.48,
        385.77,
        386.07,
        386.37,
        386.66,
        386.96,
        387.25,
        387.55,
        387.84,
        388.13,
        388.42,
        388.72,
        389.01,
        389.31,
        389.61,
        389.90,
        390.19,
        390.48,
    ]  # 390.48 Ohm Pt100 resistance at 850 deg C

    def interp_resist_to_temp(resist):
        try:
            import numpy as np

            return np.interp(resist, pt100.resistance_vals, pt100.temperature_vals)
        except:
            if resist < pt100.resistance_vals[0] or resist > pt100.resistance_vals[-1]:
                raise ValueError("Value out of range")
            i = 0
            while resist > pt100.resistance_vals[i + 1]:
                i += 1
            delta_r = pt100.resistance_vals[i + 1] - pt100.resistance_vals[i]
            delta_t = 1.0
            cur_dr = resist - pt100.resistance_vals[i]
            temp = pt100.temperature_vals[i] + cur_dr / delta_r
            return temp


if "__main__" == __name__:
    print(TempSensorDriver.getTemp_degc(0))
