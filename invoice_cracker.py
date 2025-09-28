import io
from multiprocessing import Pool, Manager
# from PyPDF2 import PdfReader # TOO SLOW!
import pikepdf
import time

def valid_cpf(cpf):
    numbers = [int(digit) for digit in cpf]
    for length in [10,11]:
        verification_digit = (sum(a * b for a, b in zip(numbers, range(length, 1, -1))) * 10 % 11) % 10
        if length == 10:
            numbers.append(verification_digit)
        cpf += str(verification_digit)
    return cpf

def generate_all_possible_cpfs(chunk):
    print(f"Generating CPFs combinations on thread {chunk}...")
    SIZE = int(1_000_000_000 / WORKERS)
    start_time = time.time()
    cpfs = []
    for i in range(chunk * SIZE, chunk * SIZE + SIZE):
        cpfs.append(valid_cpf(str(i).zfill(9)))
    print(f"Finished processing on thread {chunk} | Total time: {time.time() - start_time:.4f} seconds")
    print(f"First CPF: {cpfs[0]} | Last CPF: {cpfs[-1]} | Total CPFs: {len(cpfs)}")
    return None

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

def run_in_parallel(func, tasks):
    start_time = time.time()
    with Pool(processes=WORKERS) as pool:
        for res in pool.imap_unordered(func, tasks):
            try:
                if res:
                    pool.terminate()
                    break
            except Exception as e:
                print(f"Error: {e}")
    print(f"All done!! | Total time: {time.time() - start_time:.4f} seconds!")

def run_in_parallel_generate_cpfs():
    tasks = [i for i in range(WORKERS)]
    run_in_parallel(generate_all_possible_cpfs, tasks)

def run_in_parallel_find_pdf_password(pdf_file_path):
    mgr = Manager()
    found_event = mgr.Event()
    pdf_file = read_file(pdf_file_path)
    tasks = [(i, pdf_file, found_event) for i in range(0, WORKERS)]
    run_in_parallel(find_pdf_password, tasks)

WORKERS = 32

def main():
    run_in_parallel_generate_cpfs()
    # run_in_parallel_find_pdf_password("invoice.pdf")

if __name__ == "__main__":
    main()