import io
from multiprocessing import Pool, Manager
# from PyPDF2 import PdfReader # TOO SLOW!
import pikepdf
import time

def valid_cpf(cpf):
    numbers = [int(digit) for digit in cpf if digit.isdigit()]
    for i in range(0,2):
        sum_of_products = sum(a*b for a, b in zip(numbers, range(len(numbers) + 1, 1, -1)))
        numbers.append((sum_of_products * 10 % 11) % 10)
    return cpf + "".join([str(number) for number in numbers[-2:]])

WORKERS = 32

def get_all_possible_cpfs(chunk):
    SIZE = int(1_000_000_000 / WORKERS)
    start_time = time.time()
    cpfs = []
    for i in range(chunk * SIZE, chunk * SIZE + SIZE):
        cpfs.append(valid_cpf(str(i).zfill(9)))
    print(f"We are on thread {chunk} | Total time: {time.time() - start_time:.4f} seconds!")
    print(cpfs[:10])
    print(cpfs[-10:])
    print(len(cpfs))
    return cpfs

def find_pdf_password(args):
    chunk, pdf_file, found_event = args
    SIZE = int(1_000_000_000 / WORKERS)
    start_time = time.time()
    counter = 0
    COUNTER_ITERATION = 100_000
    for i in range(chunk * SIZE, chunk * SIZE + SIZE):
        possible_cpf = valid_cpf(str(i).zfill(9))
        if counter % COUNTER_ITERATION == 0:
            print(f"We are on thread {chunk} and cpf combination {possible_cpf[:9]} | Counter: {counter // COUNTER_ITERATION} | Total time: {time.time() - start_time:.4f} seconds!")
        counter += 1
        try:
            reader = pikepdf.open(pdf_file, password=valid_cpf(str(i).zfill(9)))
        except pikepdf.PasswordError:
            continue
        file = open("cpf.txt", "w")
        print(possible_cpf, file=file)
        file.close()
        found_event.set()
        return possible_cpf
    return None

def read_file(file):
    with open(file, "rb") as f:
        file_bytes = f.read()
        return io.BytesIO(file_bytes)

def main():
    start_time = time.time()
    mgr = Manager()
    found_event = mgr.Event()
    pdf_file = read_file("invoice.pdf")
    tasks = [(i, pdf_file, found_event) for i in range(0, WORKERS)]
    with Pool(processes=WORKERS) as pool:
        for res in pool.imap_unordered(find_pdf_password, tasks):
            try:
                if res:
                    found_pwd = res
                    print(f"Found password: {found_pwd}")
                    pool.terminate()
                    break
            finally:
                pool.join()

    print(f"All done!! | Total time: {time.time() - start_time:.4f} seconds!")

if __name__ == "__main__":
    main()