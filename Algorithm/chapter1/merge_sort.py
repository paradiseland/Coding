def merge(A, p, q, r):
	n1 = p - q + 1 # contain q
	n2 = r - q     # not contain q
	L = A[p:q+1]
	R = A[q+1:r+1]
	L.append(float('inf'))
	R.append(float('inf'))
	i = 0
	j = 0
	for k in range(p, r+1):
		if L[i] <= R[j]:
			A[k] = L[i]
			i += 1
		else:
			A[k] = R[j]
			j += 1
   
	return 


def merge_sort(A, p, r):
	if p < r:
		q = int((p+r)/2)
		merge_sort(A, p, q)
		merge_sort(A, q+1, r)
		merge(A, p , q, r)
	return A

if __name__ == "__main__":
	print(merge([1,3,7,8, 2,6,10,21],0,3,7 ))
	import random
	a = list(range(10))
	random.shuffle(a)
	print(a)
	print(merge_sort(a, 0, len(a)-1))
