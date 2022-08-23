#!/usr/env/bin python3
import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser()
    # 要产生的图片的数量
    parser.add_argument('--num_img', type=int, default=5000, help="Number of images to generate")
    # 每个图中的字数（中文）或者词语数量（英文），对于英文语料，默认长度是3
    parser.add_argument('--length', type=int, default=10,
                        help='Chars(chn) or words(eng) in a image. For eng corpus mode, default length is 3')
    # 训练一个CRNN模型时，一个图中最大字符数量应该小于最后一层CNN层的宽度
    parser.add_argument('--clip_max_chars', action='store_true', default=False,
                        help='For training a CRNN model, max number of chars in an image'
                             'should less then the width of last CNN layer.')

    parser.add_argument('--img_height', type=int, default=210)
    # 如果是0，则输出图像会有不同的宽度
    parser.add_argument('--img_width', type=int, default=0,
                        help="If 0, output images will have different width")
    # 允许在图像中出现的字符集
    parser.add_argument('--chars_file', type=str, default='./data/chars/metrics.txt',
                        help='Chars allowed to be appear in generated images.')
    # 设置渲染图像时的参数
    parser.add_argument('--config_file', type=str, default='./configs/default.yaml',
                        help='Set the parameters when rendering images')
    # 要是用的字体文件的路径
    parser.add_argument('--fonts_list', type=str, default='./data/fonts_list/eng.txt',
                        help='Fonts file path to use')
    # 背景图文件夹，对应于yaml配置文件
    parser.add_argument('--bg_dir', type=str, default='./data/bg',
                        help="Some text images(according to your config in yaml file) will"
                             "use pictures in this folder as background")
    # 当语料库模式为chn或eng时，图像上的文本将从语料库中随机选取。递归地查找语料库目录中的所有txt文件
    parser.add_argument('--corpus_dir', type=str, default="./data/list_corpus",
                        help='When corpus_mode is chn or eng, text on image will randomly selected from corpus.'
                             'Recursively find all txt file in corpus_dir')
    # 不同的语料库类型有不同的Load/get_sample方法，random：随机从字符文件里选择字符，chn：从语料库里选择连续的字符，eng：从语料库中选择连续的词语，自带空格。
    parser.add_argument('--corpus_mode', type=str, default='list', choices=['random', 'chn', 'eng', 'list'],
                        help='Different corpus type have different load/get_sample method'
                             'random: random pick chars from chars file'
                             'chn: pick continuous chars from corpus'
                             'eng: pick continuous words from corpus, space is included in label')
    #
    parser.add_argument('--output_dir', type=str, default='./output/', help='Images save dir')
    # 输出图像被保存在 output_dir/{tag}目录下
    parser.add_argument('--tag', type=str, default='default3', help='output images are saved under output_dir/{tag} dir')
    # 输出未被裁减的图像（cropped 裁剪的） 变换时中间过程的产物
    parser.add_argument('--debug', action='store_true', default=False, help="output uncroped image")

    parser.add_argument('--viz', action='store_true', default=False)
    # 检查生成图像时字体对字符的支持
    parser.add_argument('--strict', action='store_true', default=False,
                        help="check font supported chars when generating images")
    # 使用cuda
    parser.add_argument('--gpu', action='store_true', default=False, help="use CUDA to generate image")
    # 产生图像时使用的进程数量。None的话，使用所有的CPU核数。
    parser.add_argument('--num_processes', type=int, default=4,
                        help="Number of processes to generate image. If None, use all cpu cores")

    flags, _ = parser.parse_known_args()
    flags.save_dir = os.path.join(flags.output_dir, flags.tag)

    if os.path.exists(flags.bg_dir):
        num_bg = len(os.listdir(flags.bg_dir))
        flags.num_bg = num_bg

    if not os.path.exists(flags.save_dir):
        os.makedirs(flags.save_dir)

    if flags.num_processes == 1:
        parser.error("num_processes min value is 2")

    return flags


if __name__ == '__main__':
    args = parse_args()
    print(args.corpus_dir)
