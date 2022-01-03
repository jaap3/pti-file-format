#!/usr/bin/env python3
"""Inspect Polyend Tracker .pti files."""
from __future__ import annotations

import enum
import functools
import glob
import io
import json
import os
import struct

from typing import Any, Callable

##
# Discover header length by finding PCM data offset
##

with open("./test.wav", "rb") as f:
    test_wav_data = f.read()

with open("./test.pti", "rb") as f:
    test_pti_data = f.read()

WAV_HEADER_LENGTH = 44

test_wav_header = test_wav_data[0:WAV_HEADER_LENGTH]
test_wav_audio = test_wav_data[WAV_HEADER_LENGTH:]

# Find .pti header length
# PTI_HEADER_LENGTH = test_pti_data.index(test_wav_audio)  # 392
PTI_HEADER_LENGTH = 392


@functools.singledispatch
def get_header(value: object) -> bytes:
    """Return .pti header."""
    raise NotImplementedError


@functools.singledispatch
def get_audio(value: object) -> bytes:
    """Return .pti audio."""
    raise NotImplementedError


@get_header.register(bytes)
def _(value: bytes) -> bytes:
    """Return header from .pti bytestring."""
    return value[0:PTI_HEADER_LENGTH]


@get_audio.register(bytes)
def _(value: bytes) -> bytes:
    """Return audio from .pti bytestring."""
    return value[PTI_HEADER_LENGTH:]


test_pti_header = get_header(test_pti_data)
test_pti_audio = get_audio(test_pti_data)

assert test_pti_audio == test_wav_audio


##
# Get header and audio from open .pti file
##


@get_header.register(io.BufferedIOBase)
def _(value: io.BufferedIOBase) -> bytes:
    """Return header from .pti file."""
    value.seek(0)
    return value.read(PTI_HEADER_LENGTH)


@get_audio.register(io.BufferedIOBase)
def _(value: io.BufferedIOBase) -> bytes:
    """Return audio from .pti file."""
    value.seek(PTI_HEADER_LENGTH)
    return value.read()


@get_header.register(str)
def _(value: str) -> bytes:
    """Return header from path to .pti file."""
    with open(value, "rb") as f:
        return get_header(f)


@get_audio.register(str)
def _(value: str) -> bytes:
    """Return audio from path to .pti file."""
    with open(value, "rb") as f:
        return get_audio(f)


# Headers of test .pti files
pti_headers = {
    "instrument_name": get_header("./test/1 ABCDEFGHIJKLMNOPQRSTUVWXYZabcde.pti"),
    "volume_max": get_header("./test/2 test.pti"),
    "volume_null": get_header("./test/3 test.pti"),
    "volume_min": get_header("./test/4 test.pti"),
    "panning_min": get_header("./test/5 test.pti"),
    "panning_max": get_header("./test/6 test.pti"),
    "tune_min": get_header("./test/7 test.pti"),
    "tune_max": get_header("./test/8 test.pti"),
    "tune_neg12": get_header("./test/16 test.pti"),
    "finetune_min": get_header("./test/9 test.pti"),
    "finetune_max": get_header("./test/10 test.pti"),
    "filter_lp": get_header("./test/11 test.pti"),
    "filter_hp": get_header("./test/12 test.pti"),
    "filter_bp": get_header("./test/13 test.pti"),
    "overdrive": get_header("./test/14 test.pti"),
    "bit_depth": get_header("./test/15 test.pti"),
    "lp_cutoff": get_header("./test/17 test.pti"),
    "hp_cutoff_rez": get_header("./test/18 test.pti"),
    "bp_cutoff_rez": get_header("./test/19 test.pti"),
    "reverb_max": get_header("./test/20 test.pti"),
    "reverb_min": get_header("./test/22 test.pti"),
    "delay_max": get_header("./test/21 test.pti"),
    "delay_min": get_header("./test/23 test.pti"),
    "loop_fwd": get_header("./test/24 test.pti"),
    "loop_bkwd": get_header("./test/25 test.pti"),
    "loop_pingpong": get_header("./test/26 test.pti"),
    "play_slice": get_header("./test/27 test.pti"),
    "play_beat_slice": get_header("./test/28 test.pti"),
    "play_wavetable": get_header("./test/29 test.pti"),
    "play_granular": get_header("./test/30 test.pti"),
    "volume_automation_off": get_header("./test/31 test.pti"),
    "volume_automation_lfo": get_header("./test/32 test.pti"),
    "panning_automation_envelope": get_header("./test/33 test.pti"),
    "panning_automation_lfo": get_header("./test/34 test.pti"),
    "cutoff_automation_envelope": get_header("./test/35 test.pti"),
    "cutoff_automation_lfo": get_header("./test/36 test.pti"),
    "wavetable_automation_envelope": get_header("./test/37 test.pti"),
    "wavetable_automation_lfo": get_header("./test/38 test.pti"),
    "granular_pos_automation_envelope": get_header("./test/39 test.pti"),
    "granular_pos_automation_lfo": get_header("./test/40 test.pti"),
    "finetune_envelope": get_header("./test/41 test.pti"),
    "finetune_lfo": get_header("./test/42 test.pti"),
    "filter_defaults": get_header("./filter-test/1 test.pti"),
    "lp_100_0": get_header("./filter-test/2 test.pti"),
    "lp_50_0": get_header("./filter-test/3 test.pti"),
    "lp_0_0": get_header("./filter-test/4 test.pti"),
    "lp_100_100": get_header("./filter-test/5 test.pti"),
    "lp_100_50": get_header("./filter-test/6 test.pti"),
    "lp_50_50": get_header("./filter-test/7 test.pti"),
    "lp_0_100": get_header("./filter-test/8 test.pti"),
    "lp_0_50": get_header("./filter-test/9 test.pti"),
    "hp_100_0": get_header("./filter-test/10 test.pti"),
    "hp_50_0": get_header("./filter-test/11 test.pti"),
    "hp_0_0": get_header("./filter-test/12 test.pti"),
    "hp_100_100": get_header("./filter-test/13 test.pti"),
    "hp_100_50": get_header("./filter-test/14 test.pti"),
    "hp_50_50": get_header("./filter-test/15 test.pti"),
    "hp_0_100": get_header("./filter-test/16 test.pti"),
    "hp_0_50": get_header("./filter-test/17 test.pti"),
    "vol_env_attack_10": get_header("./envelope-test/2 test.pti"),
    "vol_env_attack_5": get_header("./envelope-test/3 test.pti"),
    "vol_env_decay_10": get_header("./envelope-test/4 test.pti"),
    "vol_env_decay_5": get_header("./envelope-test/5 test.pti"),
    "vol_env_sustain_50": get_header("./envelope-test/6 test.pti"),
    "vol_env_sustain_0": get_header("./envelope-test/7 test.pti"),
    "vol_env_release_10": get_header("./envelope-test/8 test.pti"),
    "vol_env_release_0": get_header("./envelope-test/9 test.pti"),
    "vol_env_amount_50": get_header("./envelope-test/10 test.pti"),
    "vol_env_amount_0": get_header("./envelope-test/11 test.pti"),
    "vol_lfo_rev_saw": get_header("./lfo-test/2 test.pti"),
    "vol_lfo_saw": get_header("./lfo-test/3 test.pti"),
    "vol_lfo_square": get_header("./lfo-test/4 test.pti"),
    "vol_lfo_random": get_header("./lfo-test/5 test.pti"),
    "vol_lfo_16_steps": get_header("./lfo-test/6 test.pti"),
    "vol_lfo_6_steps": get_header("./lfo-test/7 test.pti"),
    "vol_lfo_3_2_steps": get_header("./lfo-test/8 test.pti"),
    "vol_lfo_1_64_steps": get_header("./lfo-test/9 test.pti"),
    "vol_lfo_amount_100": get_header("./lfo-test/10 test.pti"),
    "vol_lfo_amount_0": get_header("./lfo-test/11 test.pti"),
    "pan_lfo_rev_saw": get_header("./lfo-test/12 test.pti"),
    "pan_lfo_rev_random": get_header("./lfo-test/13 test.pti"),
    "pan_lfo_1_48_step": get_header("./lfo-test/14 test.pti"),
    "pan_lfo_1_128_steps": get_header("./lfo-test/15 test.pti"),
    "pan_lfo_24_steps": get_header("./lfo-test/16 test.pti"),
    "pan_lfo_amount_80": get_header("./lfo-test/17 test.pti"),
    "pan_lfo_amount_66": get_header("./lfo-test/18 test.pti"),
    "pan_lfo_amount_25": get_header("./lfo-test/19 test.pti"),
    "pan_lfo_amount_10": get_header("./lfo-test/20 test.pti"),
    "pan_lfo_amount_100": get_header("./lfo-test/21 test.pti"),
    "cutoff_lfo_square_96_steps_amount38": get_header("./lfo-test/22 test.pti"),
    "wavetable_lfo_random_2_steps_amount_8": get_header("./lfo-test/23 test.pti"),
    "granular_lfo_saw_32_steps_amount_90": get_header("./lfo-test/24 test.pti"),
    "finetune_lfo_square_3_steps_amount_100": get_header("./lfo-test/25 test.pti"),
    "1-shot-start-002": get_header("./playback-test/2 test.pti"),
    "1-shot-start-0025": get_header("./playback-test/3 test.pti"),
    "1-shot-start-0125": get_header("./playback-test/4 test.pti"),
    "1-shot-end-02": get_header("./playback-test/5 test.pti"),
    "1-shot-end-0125": get_header("./playback-test/6 test.pti"),
    "forward-loop-start-0025-loop-start-005": get_header("./playback-test/8 test.pti"),
    "forward-loop-end-02-loop-end-018": get_header("./playback-test/9 test.pti"),
    "backward-loop-start-0033-loop-start-01111-end-0234-loop-end-0197": get_header("./playback-test/10 test.pti"),
    "pingpong-loop-start-0025-loop-start-0033-end-0250-loop-end-0190": get_header("./playback-test/11 test.pti"),
    "slice-1-2-adjust-0025-2-2-adjust-008": get_header("./playback-test/12 test.pti"),
    "48-slices": get_header("./playback-test/24 test.pti"),
    "wavetable_window_32": get_header("./playback-test/28 test.pti"),
    "wavetable_window_512": get_header("./playback-test/29 test.pti"),
    "wavetable_window_1024_position_1": get_header("./playback-test/30 test.pti"),
    "wavetable_window_32_position_343": get_header("./playback-test/31 test.pti"),
    "wavetable_window_1024_position_9": get_header("./playback-test/32 test.pti"),
    "granular_loop_backward": get_header("./playback-test/33 test.pti"),
    "granular_loop_pingpong": get_header("./playback-test/34 test.pti"),
    "granular_shape_triangle": get_header("./playback-test/35 test.pti"),
    "granular_shape_gauss": get_header("./playback-test/36 test.pti"),
    "granular_lenght_1_min": get_header("./playback-test/37 test.pti"),
    "granular_lenght_250_max": get_header("./playback-test/38 test.pti"),
    "granular_position_250_max_lenght_20": get_header("./playback-test/39 test.pti"),
    "10ms": get_header("./sample-test/1 test-10ms.pti"),
    "250ms": get_header("./sample-test/2 test-250ms.pti"),
    "1000ms": get_header("./sample-test/3 test-1000ms.pti"),
    "5000ms": get_header("./sample-test/4 test-5000ms.pti"),
    "10000ms": get_header("./sample-test/5 test-10000ms.pti"),
}


@enum.unique
class HeaderOffset(enum.IntEnum):
    """Index to values in a .pti header."""

    IS_WAVETABLE = 20
    NAME = 21
    SAMPLE_LENGTH = 60
    # Wavetable
    WAVETABLE_WINDOW_SIZE = 64
    WAVETABLE_TOTAL_POSITIONS = 68
    # Sample
    SAMPLE_PLAYBACK = 76
    PLAYBACK_START = 78
    LOOP_START = 80
    LOOP_END = 82
    PLAYBACK_END = 84
    WAVETABLE_POSITION = 88
    # Volume envelope
    VOLUME_ENVELOPE_AMOUNT = 92
    VOLUME_ENVELOPE_ATTACK = 98
    VOLUME_ENVELOPE_DECAY = 102
    VOLUME_ENVELOPE_SUSTAIN = 104
    VOLUME_ENVELOPE_RELEASE = 108
    # Volume automation
    VOLUME_AUTOMATION = 110
    # Panning envelope
    PANNING_ENVELOPE_AMOUNT = 112
    PANNING_ENVELOPE_ATTACK = 118
    PANNING_ENVELOPE_DECAY = 122
    PANNING_ENVELOPE_SUSTAIN = 124
    PANNING_ENVELOPE_RELEASE = 128
    # Panning automation
    PANNING_AUTOMATION = 130
    # Cutoff envelope
    CUTOFF_ENVELOPE_AMOUNT = 132
    CUTOFF_ENVELOPE_ATTACK = 138
    CUTOFF_ENVELOPE_DECAY = 142
    CUTOFF_ENVELOPE_SUSTAIN = 144
    CUTOFF_ENVELOPE_RELEASE = 148
    # Cutoff automation
    CUTOFF_AUTOMATION = 150
    # Wavetable position envelope
    WAVETABLE_POSITION_ENVELOPE_AMOUNT = 152
    WAVETABLE_POSITION_ENVELOPE_ATTACK = 158
    WAVETABLE_POSITION_ENVELOPE_DECAY = 162
    WAVETABLE_POSITION_ENVELOPE_SUSTAIN = 164
    WAVETABLE_POSITION_ENVELOPE_RELEASE = 168
    # Wavetable position automation
    WAVETABLE_POSITION_AUTOMATION = 170
    # Granular position envelope
    GRANULAR_POSITION_ENVELOPE_AMOUNT = 172
    GRANULAR_POSITION_ENVELOPE_ATTACK = 178
    GRANULAR_POSITION_ENVELOPE_DECAY = 182
    GRANULAR_POSITION_ENVELOPE_SUSTAIN = 184
    GRANULAR_POSITION_ENVELOPE_RELEASE = 188
    # Granular position automation
    GRANULAR_POSITION_AUTOMATION = 190
    # Finetune envelope
    FINETUNE_ENVELOPE_AMOUNT = 192
    FINETUNE_ENVELOPE_ATTACK = 198
    FINETUNE_ENVELOPE_DECAY = 202
    FINETUNE_ENVELOPE_SUSTAIN = 204
    FINETUNE_ENVELOPE_RELEASE = 208
    # Finetune automation
    FINETUNE_AUTOMATION = 210
    # Volume LFO
    VOLUME_LFO_TYPE = 212
    VOLUME_LFO_STEPS = 213
    VOLUME_LFO_AMOUNT = 216
    # Panning automation LFO
    PANNING_LFO_TYPE = 220
    PANNING_LFO_STEPS = 221
    PANNING_LFO_AMOUNT = 224
    # Cutoff automation LFO
    CUTOFF_LFO_TYPE = 228
    CUTOFF_LFO_STEPS = 229
    CUTOFF_LFO_AMOUNT = 232
    # Wavetable position automation LFO
    WAVETABLE_POSITION_LFO_TYPE = 236
    WAVETABLE_POSITION_LFO_STEPS = 237
    WAVETABLE_POSITION_LFO_AMOUNT = 240
    # Granular position automation LFO
    GRANULAR_POSITION_LFO_TYPE = 244
    GRANULAR_POSITION_LFO_STEPS = 245
    GRANULAR_POSITION_LFO_AMOUNT = 248
    # Finetune automation LFO
    FINETUNE_LFO_TYPE = 252
    FINETUNE_LFO_STEPS = 253
    FINETUNE_LFO_AMOUNT = 256
    # Filter
    FILTER_CUTOFF = 260
    FILTER_RESONANCE = 264
    FILTER_TYPE = 268
    # Instrument parameters
    TUNE = 270
    FINETUNE = 271
    VOLUME = 272
    PANNING = 276
    # Effects
    DELAY_SEND = 278
    # Slices
    SLICE_N = 280
    NUM_SLICES = 376
    # Granular
    GRANULAR_LENGTH = 378
    GRANULAR_POSITION = 380
    GRANULAR_SHAPE = 382
    GRANULAR_LOOP_MODE = 383
    # More effects
    REVERB_SEND = 384
    OVERDRIVE = 385
    BIT_DEPTH = 386


@enum.unique
class HeaderStruct(struct.Struct, enum.Enum):
    """
    Struct format strings to unpack values from a .pti file header.

    Use the HeaderOffset enum to find the offset to unpack from.
    """

    IS_WAVETABLE = "<?"
    NAME = "<31s"
    SAMPLE_LENGTH = "<L"
    # Wavetable
    WAVETABLE_WINDOW_SIZE = "<H"
    WAVETABLE_TOTAL_POSITIONS = "<H"
    # Sample
    SAMPLE_PLAYBACK = "<B"
    PLAYBACK_START = "<H"
    LOOP_START = "<H"
    LOOP_END = "<H"
    PLAYBACK_END = "<H"
    WAVETABLE_POSITION = "<H"
    # Volume envelope
    VOLUME_ENVELOPE_AMOUNT = "<f"
    VOLUME_ENVELOPE_ATTACK = "<H"
    VOLUME_ENVELOPE_DECAY = "<H"
    VOLUME_ENVELOPE_SUSTAIN = "<f"
    VOLUME_ENVELOPE_RELEASE = "<H"
    # Volume automation
    VOLUME_AUTOMATION = "<2s"
    # Panning envelope
    PANNING_ENVELOPE_AMOUNT = "<f"
    PANNING_ENVELOPE_ATTACK = "<H"
    PANNING_ENVELOPE_DECAY = "<H"
    PANNING_ENVELOPE_SUSTAIN = "<f"
    PANNING_ENVELOPE_RELEASE = "<H"
    # Panning automation
    PANNING_AUTOMATION = "<2s"
    # Cutoff envelope
    CUTOFF_ENVELOPE_AMOUNT = "<f"
    CUTOFF_ENVELOPE_ATTACK = "<H"
    CUTOFF_ENVELOPE_DECAY = "<H"
    CUTOFF_ENVELOPE_SUSTAIN = "<f"
    CUTOFF_ENVELOPE_RELEASE = "<H"
    # Cutoff automation
    CUTOFF_AUTOMATION = "<2s"
    # Wavetable position envelope
    WAVETABLE_POSITION_ENVELOPE_AMOUNT = "<f"
    WAVETABLE_POSITION_ENVELOPE_ATTACK = "<H"
    WAVETABLE_POSITION_ENVELOPE_DECAY = "<H"
    WAVETABLE_POSITION_ENVELOPE_SUSTAIN = "<f"
    WAVETABLE_POSITION_ENVELOPE_RELEASE = "<H"
    # Wavetable position automation
    WAVETABLE_POSITION_AUTOMATION = "<2s"
    # Granular position envelope
    GRANULAR_POSITION_ENVELOPE_AMOUNT = "<f"
    GRANULAR_POSITION_ENVELOPE_ATTACK = "<H"
    GRANULAR_POSITION_ENVELOPE_DECAY = "<H"
    GRANULAR_POSITION_ENVELOPE_SUSTAIN = "<f"
    GRANULAR_POSITION_ENVELOPE_RELEASE = "<H"
    # Granular position automation
    GRANULAR_POSITION_AUTOMATION = "<2s"
    # Finetune envelope
    FINETUNE_ENVELOPE_AMOUNT = "<f"
    FINETUNE_ENVELOPE_ATTACK = "<H"
    FINETUNE_ENVELOPE_DECAY = "<H"
    FINETUNE_ENVELOPE_SUSTAIN = "<f"
    FINETUNE_ENVELOPE_RELEASE = "<H"
    # Finetune automation
    FINETUNE_AUTOMATION = "<2s"
    # Volume LFO
    VOLUME_LFO_TYPE = "<B"
    VOLUME_LFO_STEPS = "<B"
    VOLUME_LFO_AMOUNT = "<f"
    # Panning automation LFO
    PANNING_LFO_TYPE = "<B"
    PANNING_LFO_STEPS = "<B"
    PANNING_LFO_AMOUNT = "<f"
    # Cutoff automation LFO
    CUTOFF_LFO_TYPE = "<B"
    CUTOFF_LFO_STEPS = "<B"
    CUTOFF_LFO_AMOUNT = "<f"
    # Wavetable position automation LFO
    WAVETABLE_POSITION_LFO_TYPE = "<B"
    WAVETABLE_POSITION_LFO_STEPS = "<B"
    WAVETABLE_POSITION_LFO_AMOUNT = "<f"
    # Granular position automation LFO
    GRANULAR_POSITION_LFO_TYPE = "<B"
    GRANULAR_POSITION_LFO_STEPS = "<B"
    GRANULAR_POSITION_LFO_AMOUNT = "<f"
    # Finetune automation LFO
    FINETUNE_LFO_TYPE = "<B"
    FINETUNE_LFO_STEPS = "<B"
    FINETUNE_LFO_AMOUNT = "<f"
    # Filter
    FILTER_CUTOFF = "<f"
    FILTER_RESONANCE = "<f"
    FILTER_TYPE = "<2s"
    # Instrument parameters
    TUNE = "<b"
    FINETUNE = "<b"
    VOLUME = "<B"
    PANNING = "<B"
    # Effects
    DELAY_SEND = "<B"
    # Slices
    SLICE_N = "<H"
    NUM_SLICES = "<B"
    # Granular loop mode
    GRANULAR_LENGTH = "<H"
    GRANULAR_POSITION = "<H"
    GRANULAR_SHAPE = "<B"
    GRANULAR_LOOP_MODE = "<B"
    # More effects
    REVERB_SEND = "<B"
    OVERDRIVE = "<B"
    BIT_DEPTH = "<B"


# Find instrument name header position
# for i, v in enumerate(test_pti_header):
#     if (iv := instrument_name_header[i]) != v:
#         print(f'{i=}, {chr(v)=}, {chr(iv)=}')
#         # i: 21-51 == instrument name
#         # i: 56-61 == ???
#         # i: 388-391 == ???

# Find volume header position
# for i, v in enumerate(test_pti_header):
#     ivmax = pti_headers['volume_max'][i]
#     ivnull = pti_headers['volume_null'][i]
#     ivmin = pti_headers['volume_min'][i]
#     if any(iv != v for iv in (ivmax, ivnull, ivmin)):
#         print(f'{i=}, {v=}, {ivmax=}, {ivnull=}, {ivmin=}')
#         # i: 272 == volume

# Find panning header position
# for i, v in enumerate(test_pti_header):
#     ivmin = pti_headers['panning_min'][i]
#     ivmax = pti_headers['panning_max'][i]
#     if any(iv != v for iv in (ivmax, ivmin)):
#         print(f'{i=}, {v=}, {ivmax=}, {ivmin=}')
#         # i: 276 == panning


def _cmp_head(
    *headers: str,
    default_header: bytes = test_pti_header,
    header_map: dict[str, bytes] = pti_headers,
) -> None:
    """Compare .pti file header(s) to the default header and show which bytes are different."""
    for i, v in enumerate(default_header):
        if 21 <= i <= 51:
            continue  # Instrument name

        ivs = {header: header_map[header][i] for header in headers}
        if any(iv != v for iv in ivs.values()):
            if i in list(HeaderOffset):
                print(HeaderOffset(i))
                print("-" * 80)

            dbg = {
                k: {
                    "int": v,
                    "bytes": repr(bytes([v])),
                }
                for k, v in ivs.items()
            }
            print(f"\n{i=}, default: int: {v} bytes: {bytes([v])!r}" f"{json.dumps(dbg, indent=2)}")


##
# Find header offsets
##

# _cmp_head('tune_min', 'tune_max', 'tune_neg12')  # 270
# _cmp_head('finetune_min', 'finetune_max')  # 271
# _cmp_head('filter_lp', 'filter_bp', 'filter_hp')  # 268 / 269
# _cmp_head('overdrive')  # 385
# _cmp_head('bit_depth')  # 386
# _cmp_head('lp_cutoff', 'hp_cutoff_rez', 'bp_cutoff_rez') # 262-263 = cutoff (???) / 264-267 = resonance (???)
# _cmp_head('reverb_max', 'reverb_min')  # 384
# _cmp_head('delay_max', 'delay_min')  # 278
# _cmp_head(
#     'loop_fwd',
#     'loop_bkwd',
#     'loop_pingpong',
#     'play_slice',
#     'play_beat_slice',
#     'play_wavetable',
#     'play_granular',
# )  # 76
# _cmp_head(
#     'volume_automation_off',
#     'volume_automation_lfo',
# ) # 110-111
# _cmp_head(
#     'panning_automation_envelope',
#     'panning_automation_lfo',
# )  # 130-131
# _cmp_head(
#     'cutoff_automation_envelope',
#     'cutoff_automation_lfo',
# )  # 150-151
# _cmp_head(
#     'wavetable_automation_envelope',
#     'wavetable_automation_lfo',
# )  # 170-171
# _cmp_head(
#     'granular_pos_automation_envelope',
#     'granular_pos_automation_lfo',
# ) # 190-191
# _cmp_head(
#     'finetune_envelope',
#     'finetune_lfo',
# ) # 210-211
# _cmp_head(
#     'lp_100_0',
#     'hp_100_0',
#     'lp_100_100',
#     'hp_100_100',
#     'lp_50_0',
#     'hp_50_0',
#     'lp_0_0',
#     'hp_0_0',
#     'lp_0_100',
#     'hp_0_100',
#     'lp_50_50',
#     'hp_50_50',
#     'lp_100_50',
#     'hp_100_50',
#     'lp_0_50',
#     'hp_0_50',
# )  # 260-263 / 263-266

# _cmp_head('vol_env_attack_10', 'vol_env_attack_5')  # 98-99
# _cmp_head('vol_env_decay_10', 'vol_env_decay_5')  # 102-103
# _cmp_head('vol_env_sustain_50', 'vol_env_sustain_0')  # 104-107
# _cmp_head('vol_env_release_10', 'vol_env_release_0')  # 108-109
# _cmp_head('vol_env_amount_50', 'vol_env_amount_0')  # 92-95

# _cmp_head('vol_lfo_rev_saw', 'vol_lfo_saw', 'vol_lfo_square', 'vol_lfo_random') # 212: 0, 1, 2, 3, 4
# _cmp_head('vol_lfo_16_steps', 'vol_lfo_6_steps', 'vol_lfo_3_2_steps', 'vol_lfo_1_64_steps') # 213: 0-23
# _cmp_head('vol_lfo_amount_100', 'vol_lfo_amount_0')  # 218-219

# _cmp_head('pan_lfo_rev_saw', 'pan_lfo_rev_random')  # 220
# _cmp_head('pan_lfo_1_48_step', 'pan_lfo_1_128_steps', 'pan_lfo_24_steps')  # 221
# _cmp_head(
#     'pan_lfo_amount_80', 'pan_lfo_amount_66', 'pan_lfo_amount_25', 'pan_lfo_amount_10', 'pan_lfo_amount_100'
# )  # 224-227
# _cmp_head('cutoff_lfo_square_96_steps_amount38')  # 228 / 228 / 232-235
# _cmp_head('wavetable_lfo_random_2_steps_amount_8')  # 236 / 237 / 240-243
# _cmp_head('granular_lfo_saw_32_steps_amount_90')  # 244 etc.
# _cmp_head('finetune_lfo_square_3_steps_amount_100')  # # 252 etc.
# _cmp_head("1-shot-start-002", "1-shot-start-0025", "1-shot-start-0125")
# _cmp_head("1-shot-end-02", "1-shot-end-0125",)
# _cmp_head(
#     "forward-loop-start-0025-loop-start-005",
#     "forward-loop-end-02-loop-end-018"
# )
# _cmp_head("backward-loop-start-0033-loop-start-01111-end-0234-loop-end-0197")
# _cmp_head("pingpong-loop-start-0025-loop-start-0033-end-0250-loop-end-0190")
# _cmp_head("slice-1-2-adjust-0025-2-2-adjust-008")
# _cmp_head("slice-1-2-adjust-0025-2-2-adjust-008", "48-slices")
# _cmp_head("granular_loop_backward", "granular_loop_pingpong")  # 383
# _cmp_head("granular_shape_triangle", "granular_shape_gauss")  # 382
# _cmp_head("wavetable_window_32", "wavetable_window_512", "wavetable_window_1024_position_1")  # 64-65
# _cmp_head(
#     "wavetable_window_1024_position_1",
#     "wavetable_window_1024_position_9",
#     "wavetable_window_32_position_343",
# )  # 88-89 = position (short)
# _cmp_head("granular_lenght_1_min", "granular_lenght_250_max", "granular_position_250_max_lenght_20")  # 378-379
# _cmp_head("10ms", "250ms", "1000ms", "5000ms", "10000ms")


def is_pti(header: bytes) -> bool:
    """Return True if a byte string has the characteristics of a .pti file header."""
    is_pti = False
    if len(header) == 392 and header[0:2] == b"TI":
        known_0 = [
            3,
            17, 18, 19,
            52, 53, 54, 55,
            66, 67,
            70, 71, 72, 73, 74, 75,
            77,
            86, 87,
            90, 91,
            96, 97,
            100, 101,
            116, 117,
            120, 121,
            136, 137,
            140, 141,
            156, 157,
            160, 161,
            176, 177,
            180, 181,
            196, 197,
            200, 201,
            214, 215,
            222, 223,
            230, 231,
            238, 239,
            246, 247,
            254, 255,
            273, 274,
            275, 277,
            279,
            387,
        ]
        for offset in known_0:
            assert (value := header[offset]) == 0, f'{offset=} {value=}'

        known_1 = [2, 4, 7, 13, 16]
        for offset in known_1:
            assert (value := header[offset]) == 1, f'{offset=} {value=}'

        known_0_or_1 = [6]
        for offset in known_0_or_1:
            assert (value := header[offset]) in {0, 1}, f'{offset=} {value=}'

        known_9 = [8, 9, 10, 11]
        for offset in known_9:
            assert (value := header[offset]) == 9, f'{offset=} {value=}'

        assert (value := header[5]) in (4, 5), f'{value=}'
        assert (value := header[12]) == 116, f'{value=}'
        assert (value := header[14]) in (102, 110), f'{value=}'
        assert (value := header[15]) == 102, f'{value=}'

        is_pti = True

    return is_pti


# Mystery bytes

# These seem to be related to the sample size, current instrument - previous instrument = instrument length
# _unknown = [56, 57, 58, 59]
# Not sure...
# _unknown = [388, 389, 390, 391]
# print(_unknown)
# print(struct.unpack('<L', bytearray([test_pti_header[n] for n in _unknown])))
# print([test_pti_header[n] for n in _unknown])
# for key, value in pti_headers.items():
#     print(key, [value[n] for n in _unknown])
#     print(key, struct.unpack('<L', bytearray([value[n] for n in _unknown])))
#
#
# for key, header in pti_headers.items():
#     print(key)
#     print(header[3])
#     is_pti(header)


# if os.path.exists('./Instruments'):
#     # https://polyend.com/files/Instruments.zip
#     for fname in glob.glob('./Instruments/**/*.pti'):
#         print(fname)
#         header = get_header(fname)
#         print(header[3])
#         is_pti(header)


def _unpack(header: bytes, field: str) -> bytes | int | float | bool:
    """Unpack a value from a .pti file header."""
    assert is_pti(header), "Not a .pti header"
    assert isinstance(
        value := HeaderStruct[field].unpack_from(header, HeaderOffset[field])[0],
        (bytes, int, float),
    ), type(value)
    return value


def _test(func: Callable[[bytes], Any], header: bytes, expected: Any) -> None:
    """Assert that calling func with the given header returns the expected value."""
    assert (value := func(header)) == expected, f"{func=} => {value=} ({expected=})"


##
# Instrument name
##


def get_name(header: bytes) -> str:
    """Return instrument name."""
    assert isinstance(value := _unpack(header, "NAME"), bytes), type(value)
    return value.rstrip(b"\x00").decode("ascii")


_test(get_name, test_pti_header, "test")
_test(get_name, pti_headers["instrument_name"], "ABCDEFGHIJKLMNOPQRSTUVWXYZabcde")


##
# Sample length
##


def get_sample_length(header: bytes) -> int:
    """Return sample length."""
    assert isinstance(value := _unpack(header, "SAMPLE_LENGTH"), int), type(value)
    assert 0 <= value <= 4294967295
    return value


_test(get_sample_length, test_pti_header, 0)
_test(get_sample_length, pti_headers["10ms"], 10 * 44.1)
_test(get_sample_length, pti_headers["250ms"], 250 * 44.1)
_test(get_sample_length, pti_headers["1000ms"], 1000 * 44.1)
_test(get_sample_length, pti_headers["5000ms"], 5000 * 44.1)
_test(get_sample_length, pti_headers["10000ms"], 10000 * 44.1)


##
# Instrument parameters
##


def get_volume(header: bytes) -> int:
    """Return volume value (0-100)."""
    assert isinstance(value := _unpack(header, "VOLUME"), int), type(value)
    assert 0 <= value <= 100, value
    return value


_test(get_volume, test_pti_header, 50)
_test(get_volume, pti_headers["volume_null"], 0)
_test(get_volume, pti_headers["volume_min"], 1)
_test(get_volume, pti_headers["volume_max"], 100)


def get_panning(header: bytes) -> int:
    """Return panning value (0-100)."""
    assert isinstance(value := _unpack(header, "PANNING"), int), type(value)
    assert 0 <= value <= 100, value
    return value


_test(get_panning, test_pti_header, 50)
_test(get_panning, pti_headers["panning_min"], 0)
_test(get_panning, pti_headers["panning_max"], 100)


def get_tune(header: bytes) -> int:
    """Return tune value (-/+24)."""
    assert isinstance(value := _unpack(header, "TUNE"), int), type(value)
    assert -24 <= value <= 24, value
    return value


_test(get_tune, test_pti_header, 0)
_test(get_tune, pti_headers["tune_min"], -24)
_test(get_tune, pti_headers["tune_max"], 24)
_test(get_tune, pti_headers["tune_neg12"], -12)


def get_finetune(header: bytes) -> int:
    """Return finetune value (-/+100)."""
    assert isinstance(value := _unpack(header, "FINETUNE"), int), type(value)
    assert -100 <= value <= 100, value
    return value


_test(get_finetune, test_pti_header, 0)
_test(get_finetune, pti_headers["finetune_min"], -100)
_test(get_finetune, pti_headers["finetune_max"], 100)


##
# Filter parameters
##


def get_filter_cutoff(header: bytes) -> float:
    """Return filter cutoff value (0.0-1.0)."""
    assert isinstance(value := _unpack(header, "FILTER_CUTOFF"), float), type(value)
    assert 0.0 <= value <= 1.0, value
    return value


_test(get_filter_cutoff, test_pti_header, 1.0)
_test(get_filter_cutoff, pti_headers["lp_100_0"], 1.0)
_test(get_filter_cutoff, pti_headers["hp_100_0"], 1.0)
_test(get_filter_cutoff, pti_headers["lp_50_0"], 0.5000002384185791)
_test(get_filter_cutoff, pti_headers["hp_50_0"], 0.5000002384185791)
_test(get_filter_cutoff, pti_headers["lp_0_0"], 0.0)
_test(get_filter_cutoff, pti_headers["hp_0_0"], 0.0)
_test(get_filter_cutoff, pti_headers["lp_100_100"], 1.0)
_test(get_filter_cutoff, pti_headers["hp_100_100"], 1.0)


def get_filter_resonance(header: bytes) -> float:
    """Return filter resonance value (0.0-+4.300000190734863)."""
    assert isinstance(value := _unpack(header, "FILTER_RESONANCE"), float), type(value)
    # This value range looks weird, but it seems to be correct...
    assert 0.0 <= value <= 4.300000190734863, value
    return value


_test(get_filter_resonance, test_pti_header, 0.0)
_test(get_filter_resonance, pti_headers["lp_100_100"], 4.300000190734863)
_test(get_filter_resonance, pti_headers["hp_100_100"], 4.300000190734863)
_test(get_filter_resonance, pti_headers["lp_100_50"], 2.150000810623169)
_test(get_filter_resonance, pti_headers["hp_100_50"], 2.1929996013641357)
_test(get_filter_resonance, pti_headers["lp_100_0"], 0.0)
_test(get_filter_resonance, pti_headers["hp_100_0"], 0.0)
_test(get_filter_resonance, pti_headers["lp_0_50"], 2.1929996013641357)
_test(get_filter_resonance, pti_headers["hp_0_50"], 2.192999839782715)


@enum.unique
class FilterType(bytes, enum.Enum):
    """Filter type."""

    # This is probably filter type (0/1/2) + on/off (0/1)
    DISABLED = b"\x00\x00"
    LOW_PASS = b"\x00\x01"
    HIGH_PASS = b"\x01\x01"
    BAND_PASS = b"\x02\x01"


def get_filter_type(header: bytes) -> FilterType:
    """Return filter type value."""
    assert isinstance(value := _unpack(header, "FILTER_TYPE"), bytes), type(value)
    return FilterType(value)


_test(get_filter_type, test_pti_header, FilterType.DISABLED)

for key in [
    "filter_lp",
    "lp_100_0",
    "lp_50_0",
    "lp_0_0",
    "lp_100_100",
    "lp_100_50",
    "lp_50_50",
    "lp_0_100",
    "lp_0_50",
]:
    _test(get_filter_type, pti_headers[key], FilterType.LOW_PASS)

for key in [
    "filter_hp",
    "hp_100_0",
    "hp_50_0",
    "hp_0_0",
    "hp_100_100",
    "hp_100_50",
    "hp_50_50",
    "hp_0_100",
    "hp_0_50",
]:
    _test(get_filter_type, pti_headers[key], FilterType.HIGH_PASS)

_test(get_filter_type, pti_headers["filter_bp"], FilterType.BAND_PASS)

##
# Effects
##


def get_overdrive(header: bytes) -> int:
    """Return overdrive value (0-100)."""
    assert isinstance(value := _unpack(header, "OVERDRIVE"), int), type(value)
    assert 0 <= value <= 100, value
    return value


_test(get_overdrive, test_pti_header, 0)
_test(get_overdrive, pti_headers["overdrive"], 100)


def get_bit_depth(header: bytes) -> int:
    """Return bit depth value (4-16)."""
    assert isinstance(value := _unpack(header, "BIT_DEPTH"), int), type(value)
    assert 4 <= value <= 16, value
    return value


_test(get_bit_depth, test_pti_header, 16)
_test(get_bit_depth, pti_headers["bit_depth"], 4)


def get_delay_send(header: bytes) -> int:
    """Return delay send value (0-100)."""
    assert isinstance(value := _unpack(header, "DELAY_SEND"), int), type(value)
    assert 0 <= value <= 100, value
    return value


_test(get_delay_send, test_pti_header, 0)
_test(get_delay_send, pti_headers["delay_min"], 1)
_test(get_delay_send, pti_headers["delay_max"], 100)


def get_reverb_send(header: bytes) -> int:
    """Return reverb send value (0-100)."""
    assert isinstance(value := _unpack(header, "REVERB_SEND"), int), type(value)
    assert 0 <= value <= 100, value
    return value


_test(get_reverb_send, test_pti_header, 0)
_test(get_reverb_send, pti_headers["reverb_min"], 1)
_test(get_reverb_send, pti_headers["reverb_max"], 100)


##
# Sample playback
##


@enum.unique
class SamplePlayback(enum.IntEnum):
    """Sample playback mode."""

    ONE_SHOT = 0
    FORWARD_LOOP = 1
    BACKWARD_LOOP = 2
    PINGPONG_LOOP = 3
    SLICE = 4
    BEAT_SLICE = 5
    WAVETABLE = 6
    GRANULAR = 7


def get_sample_playback(header: bytes) -> SamplePlayback:
    """Return sample playback mode."""
    assert isinstance(value := _unpack(header, "SAMPLE_PLAYBACK"), int), type(value)
    return SamplePlayback(value)


_test(get_sample_playback, test_pti_header, SamplePlayback.ONE_SHOT)
_test(get_sample_playback, pti_headers["loop_fwd"], SamplePlayback.FORWARD_LOOP)
_test(get_sample_playback, pti_headers["loop_bkwd"], SamplePlayback.BACKWARD_LOOP)
_test(get_sample_playback, pti_headers["loop_pingpong"], SamplePlayback.PINGPONG_LOOP)
_test(get_sample_playback, pti_headers["play_slice"], SamplePlayback.SLICE)
_test(get_sample_playback, pti_headers["play_beat_slice"], SamplePlayback.BEAT_SLICE)
_test(get_sample_playback, pti_headers["play_wavetable"], SamplePlayback.WAVETABLE)
_test(get_sample_playback, pti_headers["play_granular"], SamplePlayback.GRANULAR)


##
# Instrument automation
##


@enum.unique
class InstrumentAutomation(bytes, enum.Enum):
    """Instrument automation mode."""

    # This is probably automation type (0/1) + on/off (0/1)
    OFF = b"\x00\x00"
    ENVELOPE = b"\x00\x01"
    LFO = b"\x01\x01"


@enum.unique
class AutomationLfoType(enum.IntEnum):
    """Instrument automation LFO type."""

    REV_SAW = 0
    SAW = 1
    TRIANGLE = 2
    SQUARE = 3
    RANDOM = 4


def get_volume_automation(header: bytes) -> InstrumentAutomation:
    """Return volume automation mode."""
    assert isinstance(value := _unpack(header, "VOLUME_AUTOMATION"), bytes), type(value)
    return InstrumentAutomation(value)


_test(get_volume_automation, test_pti_header, InstrumentAutomation.ENVELOPE)
_test(
    get_volume_automation,
    pti_headers["volume_automation_off"],
    InstrumentAutomation.OFF,
)
_test(
    get_volume_automation,
    pti_headers["volume_automation_lfo"],
    InstrumentAutomation.LFO,
)


def get_panning_automation(header: bytes) -> InstrumentAutomation:
    """Return panning automation mode."""
    assert isinstance(value := _unpack(header, "PANNING_AUTOMATION"), bytes), type(value)
    return InstrumentAutomation(value)


_test(get_panning_automation, test_pti_header, InstrumentAutomation.OFF)
_test(
    get_panning_automation,
    pti_headers["panning_automation_envelope"],
    InstrumentAutomation.ENVELOPE,
)
_test(
    get_panning_automation,
    pti_headers["panning_automation_lfo"],
    InstrumentAutomation.LFO,
)


def get_cutoff_automation(header: bytes) -> InstrumentAutomation:
    """Return cutoff automation mode."""
    assert isinstance(value := _unpack(header, "CUTOFF_AUTOMATION"), bytes), type(value)
    return InstrumentAutomation(value)


_test(get_cutoff_automation, test_pti_header, InstrumentAutomation.OFF)
_test(
    get_cutoff_automation,
    pti_headers["cutoff_automation_envelope"],
    InstrumentAutomation.ENVELOPE,
)
_test(
    get_cutoff_automation,
    pti_headers["cutoff_automation_lfo"],
    InstrumentAutomation.LFO,
)


def get_wavetable_position_automation(header: bytes) -> InstrumentAutomation:
    """Return wabetable position automation mode."""
    assert isinstance(value := _unpack(header, "WAVETABLE_POSITION_AUTOMATION"), bytes), type(value)
    return InstrumentAutomation(value)


_test(get_wavetable_position_automation, test_pti_header, InstrumentAutomation.OFF)
_test(
    get_wavetable_position_automation,
    pti_headers["wavetable_automation_envelope"],
    InstrumentAutomation.ENVELOPE,
)
_test(
    get_wavetable_position_automation,
    pti_headers["wavetable_automation_lfo"],
    InstrumentAutomation.LFO,
)


def get_granular_position_automation(header: bytes) -> InstrumentAutomation:
    """Return granular position automation mode."""
    assert isinstance(value := _unpack(header, "GRANULAR_POSITION_AUTOMATION"), bytes), type(value)
    return InstrumentAutomation(value)


_test(get_granular_position_automation, test_pti_header, InstrumentAutomation.OFF)
_test(
    get_granular_position_automation,
    pti_headers["granular_pos_automation_envelope"],
    InstrumentAutomation.ENVELOPE,
)
_test(
    get_granular_position_automation,
    pti_headers["granular_pos_automation_lfo"],
    InstrumentAutomation.LFO,
)


def get_finetune_automation(header: bytes) -> InstrumentAutomation:
    """Return finetune automation mode."""
    assert isinstance(value := _unpack(header, "FINETUNE_AUTOMATION"), bytes), type(value)
    return InstrumentAutomation(value)


_test(get_finetune_automation, test_pti_header, InstrumentAutomation.OFF)
_test(
    get_finetune_automation,
    pti_headers["finetune_envelope"],
    InstrumentAutomation.ENVELOPE,
)
_test(get_finetune_automation, pti_headers["finetune_lfo"], InstrumentAutomation.LFO)


##
# Volume envelope
##


def get_volume_envelope_amount(header: bytes) -> float:
    """Return volume automation envelope amount (0.0-1.0)."""
    assert isinstance(value := _unpack(header, "VOLUME_ENVELOPE_AMOUNT"), float), type(value)
    assert 0.0 <= value <= 1.0, value
    return value


_test(get_volume_envelope_amount, test_pti_header, 1.0)
_test(get_volume_envelope_amount, pti_headers["vol_env_amount_50"], 0.5000003576278687)
_test(get_volume_envelope_amount, pti_headers["vol_env_amount_0"], 0.0)


def get_volume_envelope_attack(header: bytes) -> int:
    """Return volume automation attack amount (0-1000)."""
    assert isinstance(value := _unpack(header, "VOLUME_ENVELOPE_ATTACK"), int), type(value)
    assert 0 <= value <= 10000, value
    return value


_test(get_volume_envelope_attack, test_pti_header, 0)
_test(get_volume_envelope_attack, pti_headers["vol_env_attack_10"], 10000)
_test(get_volume_envelope_attack, pti_headers["vol_env_attack_5"], 5000)


def get_volume_envelope_decay(header: bytes) -> int:
    """Return volume automation decay amount (0-1000)."""
    assert isinstance(value := _unpack(header, "VOLUME_ENVELOPE_DECAY"), int), type(value)
    assert 0 <= value <= 10000, value
    return value


_test(get_volume_envelope_decay, test_pti_header, 0)
_test(get_volume_envelope_decay, pti_headers["vol_env_decay_10"], 10000)
_test(get_volume_envelope_decay, pti_headers["vol_env_decay_5"], 5000)


def get_volume_envelope_sustain(header: bytes) -> float:
    """Return volume sustain attack amount (0.0-1.0)."""
    assert isinstance(value := _unpack(header, "VOLUME_ENVELOPE_SUSTAIN"), float), type(value)
    assert 0.0 <= value <= 1.0, value
    return value


_test(get_volume_envelope_sustain, test_pti_header, 1.0)
_test(get_volume_envelope_sustain, pti_headers["vol_env_sustain_50"], 0.5000001788139343)
_test(get_volume_envelope_sustain, pti_headers["vol_env_sustain_0"], 0)


def get_volume_envelope_release(header: bytes) -> int:
    """Return volume automation release amount (0-1000)."""
    assert isinstance(value := _unpack(header, "VOLUME_ENVELOPE_RELEASE"), int), type(value)
    assert 0 <= value <= 10000, value
    return value


_test(get_volume_envelope_release, test_pti_header, 1000)
_test(get_volume_envelope_release, pti_headers["vol_env_release_10"], 10000)
_test(get_volume_envelope_release, pti_headers["vol_env_release_0"], 0)


# TODO: Panning/Cutoff/Wavetable/Granular/Finetune envelope


##
# Volume LFO
##


@enum.unique
class VolumeLfoSteps(enum.IntEnum):
    """Volume automation LFO steps."""

    S_24 = 0
    S_16 = 1
    S_12 = 2
    S_8 = 3
    S_6 = 4
    S_4 = 5
    S_3 = 6
    S_2 = 7
    S_3_2 = 8
    S_1 = 9
    S_3_4 = 10
    S_1_2 = 11
    S_3_8 = 12
    S_1_3 = 13
    S_1_4 = 14
    S_3_16 = 15
    S_1_6 = 16
    S_1_8 = 17
    S_1_12 = 18
    S_1_16 = 19
    S_1_24 = 20
    S_1_32 = 21
    S_1_48 = 22
    S_1_64 = 23


def get_volume_lfo_type(header: bytes) -> AutomationLfoType:
    """Return volume automation LFO type."""
    assert isinstance(value := _unpack(header, "VOLUME_LFO_TYPE"), int), type(value)
    return AutomationLfoType(value)


_test(get_volume_lfo_type, test_pti_header, AutomationLfoType.TRIANGLE)
_test(get_volume_lfo_type, pti_headers["vol_lfo_rev_saw"], AutomationLfoType.REV_SAW)
_test(get_volume_lfo_type, pti_headers["vol_lfo_saw"], AutomationLfoType.SAW)
_test(get_volume_lfo_type, pti_headers["vol_lfo_square"], AutomationLfoType.SQUARE)
_test(get_volume_lfo_type, pti_headers["vol_lfo_random"], AutomationLfoType.RANDOM)


def get_volume_lfo_steps(header: bytes) -> VolumeLfoSteps:
    """Return volume automation LFO steps."""
    assert isinstance(value := _unpack(header, "VOLUME_LFO_STEPS"), int), type(value)
    return VolumeLfoSteps(value)


_test(get_volume_lfo_steps, test_pti_header, VolumeLfoSteps.S_24)
_test(get_volume_lfo_steps, pti_headers["vol_lfo_16_steps"], VolumeLfoSteps.S_16)
_test(get_volume_lfo_steps, pti_headers["vol_lfo_6_steps"], VolumeLfoSteps.S_6)
_test(get_volume_lfo_steps, pti_headers["vol_lfo_3_2_steps"], VolumeLfoSteps.S_3_2)
_test(get_volume_lfo_steps, pti_headers["vol_lfo_1_64_steps"], VolumeLfoSteps.S_1_64)


def get_volume_lfo_amount(header: bytes) -> float:
    """Return volume automation LFO amount (0.0-1.0)."""
    assert isinstance(value := _unpack(header, "VOLUME_LFO_AMOUNT"), float), type(value)
    assert 0.0 <= value <= 1.0, value
    return value


_test(get_volume_lfo_amount, test_pti_header, 0.5)
_test(get_volume_lfo_amount, pti_headers["vol_lfo_amount_0"], 0.0)
_test(get_volume_lfo_amount, pti_headers["vol_lfo_amount_100"], 1.0)


##
# Panning LFO
##


@enum.unique
class AutomationLfoSteps(enum.IntEnum):
    """Instrument automation LFO steps (except volume)."""

    S_128 = 0
    S_96 = 1
    S_64 = 2
    S_48 = 3
    S_32 = 4
    S_24 = 5
    S_16 = 6
    S_12 = 7
    S_8 = 8
    S_6 = 9
    S_4 = 10
    S_3 = 11
    S_2 = 12
    S_3_2 = 13
    S_1 = 14
    S_3_4 = 15
    S_1_2 = 16
    S_3_8 = 17
    S_1_3 = 18
    S_1_4 = 19
    S_3_16 = 20
    S_1_6 = 21
    S_1_8 = 22
    S_1_12 = 23
    S_1_16 = 24
    S_1_24 = 25
    S_1_32 = 26
    S_1_48 = 27
    S_1_64 = 28


def get_panning_lfo_type(header: bytes) -> AutomationLfoType:
    """Return panning automation LFO type."""
    assert isinstance(value := _unpack(header, "PANNING_LFO_TYPE"), int), type(value)
    return AutomationLfoType(value)


_test(get_panning_lfo_type, test_pti_header, AutomationLfoType.TRIANGLE)
_test(get_panning_lfo_type, pti_headers["pan_lfo_rev_saw"], AutomationLfoType.REV_SAW)
_test(get_panning_lfo_type, pti_headers["pan_lfo_rev_random"], AutomationLfoType.RANDOM)


def get_panning_lfo_steps(header: bytes) -> AutomationLfoSteps:
    """Return panning automation LFO steps."""
    assert isinstance(value := _unpack(header, "PANNING_LFO_STEPS"), int), type(value)
    return AutomationLfoSteps(value)


_test(get_panning_lfo_steps, test_pti_header, AutomationLfoSteps.S_128)
_test(get_panning_lfo_steps, pti_headers["pan_lfo_1_48_step"], AutomationLfoSteps.S_1_48)
_test(get_panning_lfo_steps, pti_headers["pan_lfo_1_128_steps"], AutomationLfoSteps.S_128)
_test(get_panning_lfo_steps, pti_headers["pan_lfo_24_steps"], AutomationLfoSteps.S_24)


def get_panning_lfo_amount(header: bytes) -> float:
    """Return panning automation LFO amount (0.0-1.0)."""
    assert isinstance(value := _unpack(header, "PANNING_LFO_AMOUNT"), float), type(value)
    assert 0.0 <= value <= 1.0, value
    return value


_test(get_panning_lfo_amount, test_pti_header, 0.5)
_test(get_panning_lfo_amount, pti_headers["pan_lfo_amount_80"], 0.7999998331069946)
_test(get_panning_lfo_amount, pti_headers["pan_lfo_amount_66"], 0.6599998474121094)
_test(get_panning_lfo_amount, pti_headers["pan_lfo_amount_25"], 0.25000011920928955)
_test(get_panning_lfo_amount, pti_headers["pan_lfo_amount_10"], 0.10000001639127731)


##
# Cutoff LFO
##


def get_cutoff_lfo_type(header: bytes) -> AutomationLfoType:
    """Return cutoff automation LFO type."""
    assert isinstance(value := _unpack(header, "CUTOFF_LFO_TYPE"), int), type(value)
    return AutomationLfoType(value)


_test(get_cutoff_lfo_type, test_pti_header, AutomationLfoType.TRIANGLE)
_test(
    get_cutoff_lfo_type,
    pti_headers["cutoff_lfo_square_96_steps_amount38"],
    AutomationLfoType.SQUARE,
)


def get_cutoff_lfo_steps(header: bytes) -> AutomationLfoSteps:
    """Return cutoff automation LFO steps."""
    assert isinstance(value := _unpack(header, "CUTOFF_LFO_STEPS"), int), type(value)
    return AutomationLfoSteps(value)


_test(get_cutoff_lfo_steps, test_pti_header, AutomationLfoSteps.S_128)
_test(
    get_cutoff_lfo_steps,
    pti_headers["cutoff_lfo_square_96_steps_amount38"],
    AutomationLfoSteps.S_96,
)


def get_cutoff_lfo_amount(header: bytes) -> float:
    """Return cutoff automation LFO amount (0.0-1.0)."""
    assert isinstance(value := _unpack(header, "CUTOFF_LFO_AMOUNT"), float), type(value)
    assert 0.0 <= value <= 1.0, value
    return value


_test(get_cutoff_lfo_amount, test_pti_header, 0.5)
_test(
    get_cutoff_lfo_amount,
    pti_headers["cutoff_lfo_square_96_steps_amount38"],
    0.3800000250339508,
)


##
# Wavetable position LFO
##


def get_wavetable_position_lfo_type(header: bytes) -> AutomationLfoType:
    """Return wavetable position lfo type."""
    assert isinstance(value := _unpack(header, "WAVETABLE_POSITION_LFO_TYPE"), int), type(value)
    return AutomationLfoType(value)


_test(get_wavetable_position_lfo_type, test_pti_header, AutomationLfoType.TRIANGLE)
_test(
    get_wavetable_position_lfo_type,
    pti_headers["wavetable_lfo_random_2_steps_amount_8"],
    AutomationLfoType.RANDOM,
)


def get_wavetable_position_lfo_steps(header: bytes) -> AutomationLfoSteps:
    """Return wavetable position lfo steps."""
    assert isinstance(value := _unpack(header, "WAVETABLE_POSITION_LFO_STEPS"), int), type(value)
    return AutomationLfoSteps(value)


_test(get_wavetable_position_lfo_steps, test_pti_header, AutomationLfoSteps.S_128)
_test(
    get_wavetable_position_lfo_steps,
    pti_headers["wavetable_lfo_random_2_steps_amount_8"],
    AutomationLfoSteps.S_2,
)


def get_wavetable_position_lfo_amount(header: bytes) -> float:
    """Return wavetable position lfo amount."""
    assert isinstance(value := _unpack(header, "WAVETABLE_POSITION_LFO_AMOUNT"), float), type(value)
    assert 0.0 <= value <= 1.0
    return value


_test(get_wavetable_position_lfo_amount, test_pti_header, 0.5)
_test(
    get_wavetable_position_lfo_amount,
    pti_headers["wavetable_lfo_random_2_steps_amount_8"],
    0.08000002056360245,
)


##
# Granular position LFO
##


def get_granular_position_lfo_type(header: bytes) -> AutomationLfoType:
    """Return granular position LFO type."""
    assert isinstance(value := _unpack(header, "GRANULAR_POSITION_LFO_TYPE"), int), type(value)
    return AutomationLfoType(value)


_test(get_granular_position_lfo_type, test_pti_header, AutomationLfoType.TRIANGLE)
_test(
    get_granular_position_lfo_type,
    pti_headers["granular_lfo_saw_32_steps_amount_90"],
    AutomationLfoType.SAW,
)


def get_granular_position_lfo_steps(header: bytes) -> AutomationLfoSteps:
    """Return granular position LFO steps."""
    assert isinstance(value := _unpack(header, "GRANULAR_POSITION_LFO_STEPS"), int), type(value)
    return AutomationLfoSteps(value)


_test(get_granular_position_lfo_steps, test_pti_header, AutomationLfoSteps.S_128)
_test(
    get_granular_position_lfo_steps,
    pti_headers["granular_lfo_saw_32_steps_amount_90"],
    AutomationLfoSteps.S_32,
)


def get_granular_position_lfo_amount(header: bytes) -> float:
    """Return granular position LFO amount (0.0-1.0)."""
    assert isinstance(value := _unpack(header, "GRANULAR_POSITION_LFO_AMOUNT"), float), type(value)
    assert 0.0 <= value <= 1.0
    return value


_test(get_granular_position_lfo_amount, test_pti_header, 0.5)
_test(
    get_granular_position_lfo_amount,
    pti_headers["granular_lfo_saw_32_steps_amount_90"],
    0.8999996185302734,
)


##
# Finetune LFO
##


def get_finetune_lfo_type(header: bytes) -> AutomationLfoType:
    """Return finetune LFO type."""
    assert isinstance(value := _unpack(header, "FINETUNE_LFO_TYPE"), int), type(value)
    return AutomationLfoType(value)


_test(get_finetune_lfo_type, test_pti_header, AutomationLfoType.TRIANGLE)
_test(
    get_finetune_lfo_type,
    pti_headers["finetune_lfo_square_3_steps_amount_100"],
    AutomationLfoType.SQUARE,
)


def get_finetune_lfo_steps(header: bytes) -> AutomationLfoSteps:
    """Return finetune LFO steps."""
    assert isinstance(value := _unpack(header, "FINETUNE_LFO_STEPS"), int), type(value)
    return AutomationLfoSteps(value)


_test(get_finetune_lfo_steps, test_pti_header, AutomationLfoSteps.S_128)
_test(
    get_finetune_lfo_steps,
    pti_headers["finetune_lfo_square_3_steps_amount_100"],
    AutomationLfoSteps.S_3,
)


def get_finetune_lfo_amount(header: bytes) -> float:
    """Return finetune LFO amount (0.0-1.0)."""
    assert isinstance(value := _unpack(header, "FINETUNE_LFO_AMOUNT"), float), type(value)
    assert 0.0 <= value <= 1.0
    return value


_test(get_finetune_lfo_amount, test_pti_header, 0.5)
_test(get_finetune_lfo_amount, pti_headers["finetune_lfo_square_3_steps_amount_100"], 1.0)


##
# Playback/Loop parameters
##


def get_playback_start(header: bytes) -> int:
    """Return playback start position."""
    assert isinstance(value := _unpack(header, "PLAYBACK_START"), int), type(value)
    assert 0 <= value <= 65535, value
    return value


_test(get_playback_start, test_pti_header, 0)


def get_loop_start(header: bytes) -> int:
    """Return loop start position."""
    assert isinstance(value := _unpack(header, "LOOP_START"), int), type(value)
    assert 0 < value < 65535, value
    return value


_test(get_loop_start, test_pti_header, 1)


def get_loop_end(header: bytes) -> int:
    """Return loop end position."""
    assert isinstance(value := _unpack(header, "LOOP_END"), int), type(value)
    assert 0 < value < 65535, value
    return value


_test(get_loop_end, test_pti_header, 65534)


def get_playback_end(header: bytes) -> int:
    """Return playback end position."""
    assert isinstance(value := _unpack(header, "PLAYBACK_END"), int), type(value)
    assert 0 <= value <= 65535, value
    return value


_test(get_playback_end, test_pti_header, 65535)


##
# Slices
##


def _get_slice_adjust(header: bytes, *, nslice: int) -> int:
    """Return the start position of the requested slice."""
    assert 0 < nslice <= 48, f"{slice=}"
    offset = HeaderOffset.SLICE_N + (2 * (nslice - 1))
    value = HeaderStruct.SLICE_N.unpack_from(header, offset)[0]
    assert isinstance(value, int), type(value)
    return value


def get_slice_adjust(header: bytes, *, nslice: int) -> int:
    """Return the start position of the requested slice."""
    assert 0 < nslice <= 48, f"{nslice=}"
    value = _get_slice_adjust(header, nslice=nslice)
    # Validate result by checking the previous and next sßlice offsets
    min_value = _get_slice_adjust(header, nslice=nslice - 1) if nslice > 1 else 0
    max_value = _get_slice_adjust(header, nslice=nslice + 1) if nslice < 48 else 65535  # TODO: maybe less?
    assert min_value <= value <= max_value, f"{min_value=} < {value=} < {max_value=}"
    return value


for n in range(1, 49):
    _test(functools.partial(get_slice_adjust, nslice=n), test_pti_header, 0)


for n in range(1, 49):
    _test(
        functools.partial(get_slice_adjust, nslice=n),
        pti_headers["48-slices"],
        int(65535 / 48 * (n - 1)),
    )


def get_num_slices(header: bytes) -> int:
    """Return the number of active slices."""
    assert isinstance(value := _unpack(header, "NUM_SLICES"), int), type(value)
    assert 0 <= value <= 48, value
    return value


_test(get_num_slices, test_pti_header, 0)
_test(get_num_slices, pti_headers["slice-1-2-adjust-0025-2-2-adjust-008"], 2)
_test(get_num_slices, pti_headers["48-slices"], 48)


##
# Wavetable
##


def is_wavetable(header: bytes) -> bool:
    """Return True if Wavetable flag is set."""
    # TODO: Figure out how IS_WAVETABLE and SAMPLE_PLAYBACK are linked
    assert isinstance(value := _unpack(header, "IS_WAVETABLE"), bool), type(value)
    if value:
        assert (sample_playback := get_sample_playback(header)) == SamplePlayback.WAVETABLE, f"{sample_playback=}"
    return value


_test(is_wavetable, test_pti_header, False)
_test(is_wavetable, pti_headers["wavetable_window_1024_position_1"], True)
_test(is_wavetable, pti_headers["wavetable_window_32_position_343"], True)
_test(is_wavetable, pti_headers["wavetable_window_1024_position_9"], True)
_test(is_wavetable, pti_headers["loop_fwd"], False)
_test(is_wavetable, pti_headers["loop_bkwd"], False)
_test(is_wavetable, pti_headers["loop_pingpong"], False)
_test(is_wavetable, pti_headers["play_slice"], False)
_test(is_wavetable, pti_headers["play_beat_slice"], False)
_test(is_wavetable, pti_headers["play_wavetable"], True)
_test(is_wavetable, pti_headers["play_granular"], False)


def get_wavetable_window_size(header: bytes) -> int:
    """Return wavetable window size (32, 64, 128, 256, 1024, 2048)."""
    assert isinstance(value := _unpack(header, "WAVETABLE_WINDOW_SIZE"), int), type(value)
    assert value in {32, 64, 128, 256, 1024, 2048}, f"{value=}"
    return value


_test(get_wavetable_window_size, test_pti_header, 2048)
_test(get_wavetable_window_size, pti_headers["wavetable_window_1024_position_1"], 1024)
_test(get_wavetable_window_size, pti_headers["wavetable_window_32_position_343"], 32)
_test(get_wavetable_window_size, pti_headers["wavetable_window_1024_position_9"], 1024)


def get_wavetable_total_positions(header: bytes) -> int:
    """Return total number of wavetable positions."""
    assert isinstance(value := _unpack(header, "WAVETABLE_TOTAL_POSITIONS"), int), type(value)
    assert 0 <= value <= 65535, f"{value=}"  # TODO: figure out upper bound
    return value


_test(get_wavetable_total_positions, test_pti_header, 0)
_test(get_wavetable_total_positions, pti_headers["wavetable_window_1024_position_1"], 10)
_test(get_wavetable_total_positions, pti_headers["wavetable_window_32_position_343"], 344)


def get_wavetable_position(header: bytes) -> int:
    """Return active wavetable poisiotn."""
    assert isinstance(value := _unpack(header, "WAVETABLE_POSITION"), int), type(value)
    assert 0 <= value <= 65535, f"{value=}"  # TODO: figure out upper bound
    return value


_test(get_wavetable_position, test_pti_header, 0)
_test(get_wavetable_position, pti_headers["wavetable_window_1024_position_1"], 1)
_test(get_wavetable_position, pti_headers["wavetable_window_32_position_343"], 343)
_test(get_wavetable_position, pti_headers["wavetable_window_1024_position_9"], 9)


##
# Granular
##


@enum.unique
class GranularShape(enum.IntEnum):
    """Granular shape."""

    SQUARE = 0
    TRIANGLE = 1
    GAUSS = 2


def get_granular_shape(header: bytes) -> GranularShape:
    """Get granular shape."""
    assert isinstance(value := _unpack(header, "GRANULAR_SHAPE"), int), type(value)
    return GranularShape(value)


_test(get_granular_shape, test_pti_header, GranularShape.SQUARE)
_test(get_granular_shape, pti_headers["granular_shape_triangle"], GranularShape.TRIANGLE)
_test(get_granular_shape, pti_headers["granular_shape_gauss"], GranularShape.GAUSS)


@enum.unique
class GranularLoopMode(enum.IntEnum):
    """Granular loop mode."""

    FORWARD = 0
    BACKWARD = 1
    PINGPONG = 2


def get_granular_loop_mode(header: bytes) -> GranularLoopMode:
    """Get granular loop mode."""
    assert isinstance(value := _unpack(header, "GRANULAR_LOOP_MODE"), int), type(value)
    return GranularLoopMode(value)


_test(get_granular_loop_mode, test_pti_header, GranularLoopMode.FORWARD)
_test(
    get_granular_loop_mode,
    pti_headers["granular_loop_backward"],
    GranularLoopMode.BACKWARD,
)
_test(
    get_granular_loop_mode,
    pti_headers["granular_loop_pingpong"],
    GranularLoopMode.PINGPONG,
)


def get_granular_position(header: bytes) -> int:
    """Return granular start position."""
    assert isinstance(value := _unpack(header, "GRANULAR_POSITION"), int), type(value)
    assert 0 <= value <= 65535, value
    return value


_test(get_granular_position, test_pti_header, 0)
_test(get_granular_position, pti_headers["granular_position_250_max_lenght_20"], 65535)


def get_granular_length(header: bytes) -> int:
    """Return granular length value (44-44100)."""
    assert isinstance(value := _unpack(header, "GRANULAR_LENGTH"), int), type(value)
    assert 44 <= value <= 44100, f"{value=}"
    return value


_test(get_granular_length, test_pti_header, int(0.01 * 44100))
_test(get_granular_length, pti_headers["granular_lenght_1_min"], int(0.001 * 44100))
_test(get_granular_length, pti_headers["granular_lenght_250_max"], int(0.25 * 44100))
_test(get_granular_length, pti_headers["granular_position_250_max_lenght_20"], int(0.02 * 44100) - 1)  # Off by one
_test(get_granular_length, pti_headers["10ms"], int(0.005 * 44100))
_test(get_granular_length, pti_headers["250ms"], int(0.02 * 44100) - 1)  # Off by one
_test(get_granular_length, pti_headers["1000ms"], int(0.1 * 44100) + 2)  # Close enough
_test(get_granular_length, pti_headers["5000ms"], 44100)
_test(get_granular_length, pti_headers["10000ms"], 44100)
