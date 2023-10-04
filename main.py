import os
import requests
import zipfile

import shutil
import os

import feedparser


def remove_duplicate_lines(file_path):
  with open(file_path, 'r') as file:
    lines = file.readlines()

  # 使用集合(set)来去除重复行
  unique_lines = set(lines)

  with open(file_path, 'w') as file:
    file.writelines(unique_lines)


def extract_ip_port_from_rss(url, output_file):
  try:
    # 解析RSS订阅
    feed = feedparser.parse(url)

    # 打开文件以写入IP和Port信息
    with open(output_file, 'a') as f:
      # 遍历每个RSS项
      for entry in feed.entries:
        # 提取标题中的IP和Port信息
        title = entry.title

        # 排除包含特定文本的项
        if "Subscribe Link" in title:
          continue

        ip_start = title.find("[IP]") + len("[IP]")
        ip_end = title.find("[Port]")
        ip = title[ip_start:ip_end].strip()
        port_start = title.find("[Port]") + len("[Port]")
        port_end = title.find("[Latency]")
        port = title[port_start:port_end].strip()

        # 写入IP和Port到文件中
        f.write(f"{ip}  {port}\n")

    print(f"提取完成，并已写入文件：{output_file}")
  except Exception as e:
    print(f"发生错误：{str(e)}")


def download_and_convert(url, output_file):
  try:
    # 下载文本内容
    response = requests.get(url)
    response.raise_for_status()
    data = response.text

    # 拆分每行数据以逗号作为分隔符
    lines = data.strip().split('\n')

    # 将数据转换为IP PORT格式
    converted_data = []
    for line in lines:
      parts = line.split(',')
      if len(parts) == 3:
        ip, port, _ = parts
        converted_data.append(f"{ip}  {port}")

    # 追加转换后的数据到输出文件
    with open(output_file, 'a') as outfile:
      outfile.write('\n'.join(converted_data) + '\n')

    print("数据已转换并追加到文件:", output_file)
  except Exception as e:
    print(f"发生错误：{e}")


def move_files_to_current_directory(source_directory):
  try:
    # 获取当前目录
    target_directory = './'

    # 获取源目录中的文件列表
    file_list = os.listdir(source_directory)

    # 移动每个文件到目标目录
    for file_name in file_list:
      source_path = os.path.join(source_directory, file_name)
      target_path = os.path.join(target_directory, file_name)
      shutil.move(source_path, target_path)

    print("文件已移动到当前目录")
  except Exception as e:
    print(f"发生错误：{e}")


def download_file(url, save_path):
  try:
    response = requests.get(url)
    if response.status_code == 200:
      filename = url.split("/")[-1]
      with open(save_path, "wb") as file:
        file.write(response.content)
      print(f"Downloaded {filename} and saved as {save_path}")
      return True
    else:
      print("Failed to download file (HTTP status code:", response.status_code,
            ")")
  except Exception as e:
    print("An error occurred:", e)
  return False


def unzip_file(zip_path, extract_folder):
  with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_folder)
    print("Extracted files to:", extract_folder)


def merge_ip_files():
  ip_files = []
  for file_name in os.listdir():
    if file_name.endswith('.txt') and len(file_name.split('-')) == 3:
      ip_files.append(file_name)

  unique_ips = set()
  with open('merge-ip.txt', 'w') as ip_output:
    for ip_file in ip_files:
      ip_parts = ip_file.split('-')
      ip = ip_parts[0]
      port = ip_parts[2].split('.')[0]  # Remove .txt extension
      with open(ip_file, 'r') as ip_input:
        for line in ip_input:
          line = line.strip()
          if line:  # Skip empty lines
            ip_port = f'{line} {port}'
            if ip_port not in unique_ips:
              unique_ips.add(ip_port)
              ip_output.write(f'{ip_port}\n')
      # os.remove(ip_file)  # Delete the original txt file


def merge_ip_files2():
  ip_files = []
  for file_name in os.listdir():
    if file_name.endswith('.txt') and len(file_name.split('-')) == 3:
      ip_files.append(file_name)

  unique_ips = set()
  with open('merge-ip2.txt', 'w') as ip_output:
    for ip_file in ip_files:
      ip_parts = ip_file.split('-')
      ip = ip_parts[0]
      port = ip_parts[2].split('.')[0]  # Remove .txt extension
      with open(ip_file, 'r') as ip_input:
        for line in ip_input:
          line = line.strip()
          if line:  # Skip empty lines
            ip_port = f'{line}:{port}'
            if ip_port not in unique_ips:
              unique_ips.add(ip_port)
              ip_output.write(f'{ip_port}\n')


if __name__ == "__main__":
  url = "https://zip.baipiao.eu.org"  # 修改为你需要下载的压缩文件的 URL
  url2 = "https://github.com/hello-earth/cloudflare-better-ip/archive/refs/heads/main.zip"
  save_path = os.path.join(os.path.dirname(__file__),
                           "downloaded_file.zip")  # 修改保存路径和文件名
  save_path2 = os.path.join(os.path.dirname(__file__),
                            "downloaded_cfb_file.zip")  # 修改保存路径和文件名
  extract_folder = os.path.dirname(__file__)  # 解压缩文件的目标文件夹为当前脚本所在文件夹

  print("Downloading from:", url)
  if download_file(url, save_path):
    unzip_file(save_path, extract_folder)
    os.remove(save_path)  # 删除下载的压缩文件
  if download_file(url2, save_path2):
    unzip_file(save_path2, extract_folder)
    # 使用示例：将文件从 'cloudflare-better-ip-main/cloudflare/' 目录移动到当前目录
    # move_files_to_current_directory('cloudflare-better-ip-main/cloudflare/')
    # import os

    # 设置源目录和输出文件名
    source_directory = 'cloudflare-better-ip-main/cloudflare/'
    output_file = 'merged_output.txt'

    # 遍历目录中的所有 .txt 文件并合并它们
    with open(output_file, 'w') as merged_file:
      for file_name in os.listdir(source_directory):
        if file_name.endswith('.txt'):
          file_path = os.path.join(source_directory, file_name)
          with open(file_path, 'r') as source_file:
            merged_file.write(source_file.read())

    print("合并完成！输出文件名:", output_file)

    # 有端口 转换为 IP PORT 格式

    # 打开输入文件以及输出文件
    with open(output_file, 'r') as infile, open('cfbetter-1-443.txt',
                                                'w') as outfile:
      for line in infile:
        # 拆分每行数据以'|'作为分隔符
        parts = line.strip().split('|')
        if len(parts) >= 2:
          # 获取第一个部分中的IP和端口号
          ip_port = parts[0].strip()
          # 如果端口号在IP后面，使用空格拆分并取第一个元素
          if ':' in ip_port:
            ip, port = ip_port.split(' ')[0].split(':')
            # 写入新的格式到输出文件
            outfile.write(f"{ip}\n")

    print("格式转换完成！输出文件名:", output_file)

    os.remove(save_path2)
    os.remove(output_file)
    shutil.rmtree("cloudflare-better-ip-main")
    merge_ip_files2()
    merge_ip_files()
    # 使用示例：下载并转换数据
    url = 'https://sub.cfno1.eu.org/pure'
    output_file = 'merge-ip.txt'
    download_and_convert(url, output_file)
    # 指定RSS订阅的URL和输出文件名
    rss_url = "https://rsshub.app/telegram/channel/cf_noip?searchQuery=IP"
    # output_file = "ip_port.txt"
    # 调用函数
    extract_ip_port_from_rss(rss_url, output_file)
    # 使用示例，相同文件名作为输入和输出
    # file_path = 'merge-ip.txt'
    remove_duplicate_lines(output_file)
