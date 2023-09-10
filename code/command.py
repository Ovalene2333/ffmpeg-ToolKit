# 视频压缩
def change(
    filename='',
    a_encode='',
    v_encode='',
    newfilename='',
    resolve='',
    multiple=[],
    crop=[],
    pad=[],
    rotate='',
    flip=0,
    fps=0,
    crf=0,
    info='',
    commands='',
    profile='',
    bitrate=0,
    aspect=[],
):
    vf_enable = []
    # 多参数检测
    if resolve != '' and multiple != []:
        raise Exception("Too much args in resolve")
    else:
        vf_args = []
        if filename == '' or newfilename == '':
            raise Exception("No filename")
        # 控制分辨率的部分
        if resolve == '' and multiple == []:
            resolve_ = ''
        elif multiple == []:
            if isinstance(resolve, str):
                resolve.replace("*", "x")

                resolve_tuple = resolve.split("x")

                resolve_ = f'scale={resolve_tuple[0]}:{resolve_tuple[1]}'
                # print(resolve_)
                # 这里输入为1920*1080或1920x1080的输入格式,对应的resolve_tuple为['1920','1080']
                vf_enable = ['-vf']
            else:
                resolve_ = f'scale={resolve[0]}:{resolve[1]}'
                # 这里的输入是直接输入['1920','1080']或者[1920,1080]
                vf_enable = ['-vf']
        elif resolve == '':
            if len(multiple) != 2:
                raise Exception("Illegal input in multiple array")
            else:
                width_m = multiple[0]
                height_m = multiple[1]
                resolve_ = f'scale=iw*{width_m}:ih*{height_m}'
                vf_enable = ['-vf']
        vf_args.append(resolve_)

        # 控制裁剪的问题
        if crop == []:
            crop_ = ''
        else:
            if len(crop) == 4:
                crop_ = f'crop={crop[0]}:{crop[1]}:{crop[2]}:{crop[3]}'
            else:
                raise Exception("Illegal input for crop args")
        vf_args.append(crop_)

        # 控制填充的问题
        if pad == []:
            pad_ = ''
        else:
            if len(pad) == 5:
                pad_ = f'pad={pad[0]}:{pad[1]}:{pad[2]}:{pad[3]}:{pad[3]}'
            else:
                raise Exception("Illegal input for pad args")
        vf_args.append(pad_)

        # 控制旋转的问题
        if rotate == '':
            rotate_ = ''
        else:
            rotate_ = f'transpose={rotate}'
        vf_args.append(rotate_)

        # 控制翻转的问题

        if flip == 1:
            flip_ = f'flip={flip}'
        else:
            flip_ = ''
        vf_args.append(flip_)

        vf_args_str = ""
        for item in vf_args:
            if item != '':
                vf_args_str += f'{item},'
        if vf_args_str == '':
            vf_args_ = []
        else:
            vf_args_ = [f'''"{vf_args_str}"''']
        # print(vf_args, vf_args_str, vf_args_)
        # 上方是-vf参数的控制代码
        default_encoder = 'libx264'
        fps = int(fps)
        if fps == 0:
            fps_ = []
        else:
            fps_ = ['-r', f'{fps}']
        if a_encode == '':
            a_encode_ = ['-c:a', 'copy']
        else:
            a_encode_ = ['-c:a', a_encode]
        tmp_list = ["copy", "COPY", "Copy", '']
        if v_encode in tmp_list:
            # 没有自定义编码器，默认为空
            # v_encode_ = ['-c:v', 'libx264']
            # profile_ = ['-profile:v', 'high']
            v_encode_ = []
            profile_ = []
        else:
            # 启用了自定义编码器
            # 这里以后再写
            v_encode_ = ['-c:v', v_encode]
            if profile == '':
                profile_ = []
            else:
                profile_ = ['-profile:v', profile]
        # print(v_encode_)
        if crf == 0:
            crf_ = []
        else:
            crf_ = ['-crf', str(crf)]
        if bitrate == 0:
            bitrate_ = []
        else:
            bitrate_ = ['-b:v', str(bitrate) + "k"]
        if aspect == 'copy' or len(aspect) == 0:
            aspect_ = []
        else:
            aspect_size = f"{aspect[0]}:{aspect[1]}"
            aspect_ = ['-aspect', aspect_size]
        command = (
            ['ffmpeg', '-y', '-i', filename]
            + vf_enable
            + vf_args_
            + a_encode_
            + v_encode_
            + profile_
            + fps_
            + aspect_
            + crf_
            + [newfilename]
        )

        print(command)
        for item in command:
            print(item, end=' ')
        # subprocess.run(command)
        # if info == "Show Info":
        #     print(get_info(newfilename))
        # if commands == "Show Cmd":
        #     cmd_tmp = ''
        #     for item in command:
        #         cmd_tmp += item + " "
        #     cmd = "Original Command:" + cmd_tmp.replace(ffmpeg, "ffmpeg")
        #     return cmd
