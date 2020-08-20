# Introduction

Generate calibration image for OpenIMU. The latest calibration data in the NAS is used. Only OpenIMU330BI is supported now.

# Usage

Please refer to the doc for ```gen_cal```.

```python
def gen_cal(sn, device_name='dmu330',\
            nas_addr='\\\\10.0.0.236\\productionbackup\\dmudata\\',\
            cal_tool_dir=None,\
            out_dir=None):
    '''
    Args:
        sn: a list of SNs whose calibration images are to be created.
        device_name: dmu330 means OpenIMU330BI.
        nas_addr: a path to specify where the factory calibration data is located.
        cal_tool_dir: a path to specify where the required binary tools are located.
            If this is not specified, './cal/' is used.
        out_dir: a path to specify where the generated calibration image is stored.
            If this is not specified, 'cal_tool_dir/work/sn/' is used.
    '''
```

There is also a demo script in gen_cal.py.

```python
if __name__ == "__main__":
    sn = []
    sn_file = 'D:\\MyDocuments\\desktop\\bin_for_lianshi\\sn.txt'
    with open(sn_file, 'r') as f:
        file_contents = f.read()
        sn = file_contents.split('\n')
    gen_cal(sn, out_dir='D:\\MyDocuments\\desktop\\bin_for_lianshi')

```

The contents of sn.txt include:
```
1974001179
1974001160
1974000819
1974001185
1974001180
1974001151
1974001175
1974000858
1974001447
1974000801
1974001153
1974001433
1974001407
1974000845
1974001195
1974000840
```