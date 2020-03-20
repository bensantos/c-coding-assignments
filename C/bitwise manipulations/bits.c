/* 
 * CS 208 Lab 1: Data Lab
 * 
 * <Please put your name and userid here>
 * 
 * bits.c - Source file with your solutions to the Lab.
 *          This is the file you will hand in to your instructor.
 *
 * WARNING: Do not include the <stdio.h> header; it confuses the dlc
 * compiler. You can still use printf for debugging without including
 * <stdio.h>, although you might get a compiler warning. In general,
 * it's not good practice to ignore compiler warnings, but in this
 * case it's OK.  
 */

#if 0
/*
 * Instructions to Students:
 *
 * STEP 1: Read the following instructions carefully.
 */

You will provide your solution to the Data Lab by
editing the collection of functions in this source file.

INTEGER CODING RULES:
 
  Replace the "return" statement in each function with one
  or more lines of C code that implements the function. Your code 
  must conform to the following style:
 
  int Funct(arg1, arg2, ...) {
      /* brief description of how your implementation works */
      int var1 = Expr1;
      ...
      int varM = ExprM;

      varJ = ExprJ;
      ...
      varN = ExprN;
      return ExprR;
  }

  Each "Expr" is an expression using ONLY the following:
  1. Integer constants 0 through 255 (0xFF), inclusive. You are
      not allowed to use big constants such as 0xffffffff.
  2. Function arguments and local variables (no global variables).
  3. Unary integer operations ! ~
  4. Binary integer operations & ^ | + << >>
    
  Some of the problems restrict the set of allowed operators even further.
  Each "Expr" may consist of multiple operators. You are not restricted to
  one operator per line.

  You are expressly forbidden to:
  1. Use any control constructs such as if, do, while, for, switch, etc.
  2. Define or use any macros.
  3. Define any additional functions in this file.
  4. Call any functions.
  5. Use any other operations, such as &&, ||, -, or ?:
  6. Use any form of casting.
  7. Use any data type other than int.  This implies that you
     cannot use arrays, structs, or unions.

 
  You may assume that your machine:
  1. Uses 2s complement, 32-bit representations of integers.
  2. Performs right shifts arithmetically.
  3. Has unpredictable behavior when shifting if the shift amount
     is less than 0 or greater than 31.


EXAMPLES OF ACCEPTABLE CODING STYLE:
  /*
   * pow2plus1 - returns 2^x + 1, where 0 <= x <= 31
   */
  int pow2plus1(int x) {
     /* exploit ability of shifts to compute powers of 2 */
     return (1 << x) + 1;
  }

  /*
   * pow2plus4 - returns 2^x + 4, where 0 <= x <= 31
   */
  int pow2plus4(int x) {
     /* exploit ability of shifts to compute powers of 2 */
     int result = (1 << x);
     result += 4;
     return result;
  }

FLOATING POINT CODING RULES

For the problems that require you to implement floating-point operations,
the coding rules are less strict.  You are allowed to use looping and
conditional control.  You are allowed to use both ints and unsigneds.
You can use arbitrary integer and unsigned constants. You can use any arithmetic,
logical, or comparison operations on int or unsigned data.

You are expressly forbidden to:
  1. Define or use any macros.
  2. Define any additional functions in this file.
  3. Call any functions.
  4. Use any form of casting.
  5. Use any data type other than int or unsigned.  This means that you
     cannot use arrays, structs, or unions.
  6. Use any floating point data types, operations, or constants.


NOTES:
  1. Use the dlc (data lab checker) compiler (described in the handout) to 
     check the legality of your solutions.
  2. Each function has a maximum number of operations (integer, logical,
     or comparison) that you are allowed to use for your implementation
     of the function.  The max operator count is checked by dlc.
     Note that assignment ('=') is not counted; you may use as many of
     these as you want without penalty.
  3. Use the btest test harness to check your functions for correctness.
  4. Use the BDD checker to formally verify your functions
  5. The maximum number of ops for each function is given in the
     header comment for each function. If there are any inconsistencies 
     between the maximum ops in the writeup and in this file, consider
     this file the authoritative source.

/*
 * STEP 2: Modify the following functions according the coding rules.
 * 
 *   IMPORTANT. TO AVOID GRADING SURPRISES:
 *   1. Use the dlc compiler to check that your solutions conform
 *      to the coding rules.
 *   2. Use the BDD checker to formally verify that your solutions produce 
 *      the correct answers.
 */


#endif
/* Copyright (C) 1991-2018 Free Software Foundation, Inc.
   This file is part of the GNU C Library.

   The GNU C Library is free software; you can redistribute it and/or
   modify it under the terms of the GNU Lesser General Public
   License as published by the Free Software Foundation; either
   version 2.1 of the License, or (at your option) any later version.

   The GNU C Library is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   Lesser General Public License for more details.

   You should have received a copy of the GNU Lesser General Public
   License along with the GNU C Library; if not, see
   <http://www.gnu.org/licenses/>.  */
/* This header is separate from features.h so that the compiler can
   include it implicitly at the start of every compilation.  It must
   not itself include <features.h> or any other header that includes
   <features.h> because the implicit include comes before any feature
   test macros that may be defined in a source file before it first
   explicitly includes a system header.  GCC knows the name of this
   header in order to preinclude it.  */
/* glibc's intent is to support the IEC 559 math functionality, real
   and complex.  If the GCC (4.9 and later) predefined macros
   specifying compiler intent are available, use them to determine
   whether the overall intent is to support these features; otherwise,
   presume an older compiler has intent to support these features and
   define these macros by default.  */
/* wchar_t uses Unicode 10.0.0.  Version 10.0 of the Unicode Standard is
   synchronized with ISO/IEC 10646:2017, fifth edition, plus
   the following additions from Amendment 1 to the fifth edition:
   - 56 emoji characters
   - 285 hentaigana
   - 3 additional Zanabazar Square characters */
/* We do not support C11 <threads.h>.  */
//2
/* 
 * bitXor - x^y using only ~ and & 
 *   Example: bitXor(4, 5) = 1
 *   Legal ops: ~ &
 *   Max ops: 14
 *   Rating: 2
 */
int bitXor(int x, int y) {

    /*returns XOR of the two integers
     * uses the idea that XOR has one false and one true representation
     * They can't both be true (NOT(A&B)) and they can't both be false (NOT(NOT(A)& NOT(B))
     */
   
    int AandB = x & y;
    int notAandnotB = ~x & ~y;
    int xor = (~(AandB))&(~(notAandnotB));
    return xor;
    
}
/*
 * isTmax - returns 1 if x is the maximum, two's complement number,
 *     and 0 otherwise 
 *   Legal ops: ! ~ & ^ | +
 *   Max ops: 10
 *   Rating: 2
 */
int isTmax(int x) {
    /* if x is negative 1, the variable is set to 1. The max positive number
     * overflows into negative when adding one, so we will use this variable for 
     * comparison */
    int negative1 = !(~x);
    int compare = !((~(x+1)^x)|negative1);
    return compare;
}
/* 
 * allOddBits - return 1 if all odd-numbered bits in word set to 1
 *   where bits are numbered from 0 (least significant) to 31 (most significant)
 *   Examples allOddBits(0xFFFFFFFD) = 0, allOddBits(0xAAAAAAAA) = 1
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 12
 *   Rating: 3
 */
int allOddBits(int x) {
    /*generate a mask using addition and shifts that has a 1
     * in all for all the odd bits
     * compare against 0xFFFFFFFF and use ! to return correct value*/
    int AA = 0xAA;
    int oddBits = AA + (AA<<8) + (AA<<16) + (AA<<24);
    x =  x & oddBits;
    x = x | (~oddBits);
    return !(x ^ (~0x00));
}
/* 
 * sign - return 1 if positive, 0 if zero, and -1 if negative
 *  Examples: sign(130) = 1
 *            sign(-23) = -1
 *  Legal ops: ! ~ & ^ | + << >>
 *  Max ops: 10
 *  Rating: 3
 */
int sign(int x) {
    /*When right shifting, if the number is negative (sign bit = 1),
     * all values filled in will be one. Combined with checking to 
     * see whether or not x is zero, the return statement can
     * correctly evaluate the sign of the number*/
    return ((!!x) | x>>31);
}
//3
/* 
 * isAsciiDigit - return 1 if 0x30 <= x <= 0x39 (ASCII codes for characters '0' to '9')
 *   Example: isAsciiDigit(0x35) = 1.
 *            isAsciiDigit(0x3a) = 0.
 *            isAsciiDigit(0x05) = 0.
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 15
 *   Rating: 3
 */
int isAsciiDigit(int x) {
    /*created variable names for clarity*/
    /*bottomLimit will be 01 if the leading bit is negative (x < 0x30)
     * topLimit will be 01 if leading bit is negative (x>0x39)*/ 
    
    int bottomLimit = ((x + (~0x30 + 1))>>31);
    int topLimit = ((0x39 + (~x + 1))>>31);
    return !(bottomLimit|topLimit);

}
/* 
 * isLessOrEqual - if x <= y  then return 1, else return 0 
 *   Example: isLessOrEqual(4,5) = 1.
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 24
 *   Rating: 3
 */
int isLessOrEqual(int x, int y) {
    /*returns 1 if signs are different*/
    int diffSigns = !(x>>31)^!(y>>31);
    /*gives 1 if different signs and x is negative */
    /*if this returns 1 -> y>x so this can be a condition to test in return*/
    int signOfX = diffSigns & (x>>31);
    int yGreaterEqualToX = !diffSigns & !((y + (~x+1))>>31);
    return(signOfX | yGreaterEqualToX);

}
/* 
 * logicalNeg - implement the ! operator, using all of 
 *              the legal operators except !
 *   Examples: logicalNeg(3) = 0, logicalNeg(0) = 1
 *   Legal ops: ~ & ^ | + << >>
 *   Max ops: 12
 *   Rating: 3
 */
int logicalNeg(int x) {
    /*first condition will be all 1's if x is negative
     * second condition will be all 1's if x is positive
     * adding 1 to either of these will overflow it to zero*/
    int firstCondition = (x>>31);
    int secondCondition = ((~x+1)>>31);
    return (firstCondition | secondCondition) + 1;
}
//4
/* 
 * greatestBitPos - return a mask that marks the position of the
 *               most significant 1 bit. If x == 0, return 0
 *   Example: greatestBitPos(96) = 0x40
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 70
 *   Rating: 4 
 */
int greatestBitPos(int x) {
    /*these series of shifts make everything to the right of the most signifcant get set to 1
     *generate a mask of 1's that overlaps with the most signifcant bit while having a condition
     that works for negative numbers*/
    x = x | (x>>1);
    x = x | (x>>2);
    x = x | (x>>4);
    x = x | (x>>8);
    x = x | (x>>16);
    x = x & ((~x>>1) ^ (0x1<<31));

    return x;
}
//float
/* 
 * floatScale2 - Return bit-level equivalent of expression 2*f for
 *   floating point argument f.
*   Both the argument and result are passed as unsigned int's, but
*   When argument is NaN, return argument
e   Legal ops: Any integer/unsigned operations incl. ||, &&. also if, while
 *  eMax ops: 30
 *   Rating: 3
 */
unsigned floatScale2(unsigned uf) {
    /*when given 0 0r -0*/
    if (uf == 0 || uf == (0x01<<31)){
            return uf;
    }
    /*case for Nan (all 1's in exponent*/
    if (((uf>>23) & 0xFF) == 0xFF){
            return uf;
    }
    /*denormalized case*/
    if (((uf>>23) & 0xFF) == 0x00){
        return ((uf & (0x01<<31)) | (uf<<1)); 
    }
    return (uf + (1<<23));
    
}
/* 
 * floatFloat2Int - Return bit-level equivalent of expression (int) f
 *   for floating point argument f.
 *   Argument is passed as unsigned int, but
 *   it is to be interpreted as the bit-level representation of a
 *   single-precision floating point value.
 *   Anything out of range (including NaN and infinity) should return
 *   0x80000000u.
 *   Legal ops: Any integer/unsigned operations incl. ||, &&. also if, while
 *   Max ops: 30
 *   Rating: 3
 */
int floatFloat2Int(unsigned uf) {
    int signBit = (uf>>31) & 0x01;
    int expfield = (uf>>23) & 0xFF;
    int fractionMask =  0x1>>24;
    int fraction = uf & fractionMask;
    int newInt = (0x01<<24) + fraction;
    int holder;
    /*real exponent*/
    int exp = expfield - 127;
    
    /*check if 0*/
    if (exp<0 || expfield == 0){
        return 0;
    }
    /*overflow check*/
    if (exp >= 31 || expfield == 0xFF){
        return (0x1<<31);
    }
    /*following if statements construnct int based on value of exp*/
    if (exp > 24){
        holder = newInt<<(exp - 24);
    }

    else if (exp <=24){
        holder = newInt>>(24-exp);
    }
    
    /*check for negative*/
    if (signBit == 0x01){
        holder = -holder;
    }
    return holder;
}
/* 
 * floatPower2 - Return bit-level equivalent of the expression 2.0^x
 *   (2.0 raised to the power x) for any 32-bit integer x.
 *
 *   The unsigned value that is returned should have the identical bit
 *   representation as the single-precision floating-point number 2.0^x.
 *   If the result is too small to be represented as a denorm, return
 *   0. If too large, return +INF.
 * 
 *   Legal ops: Any integer/unsigned operations incl. ||, &&. Also if, while 
 *   Max ops: 30 
 *   Rating: 3
 */
unsigned floatPower2(int x) {
    int bias = 127;
    /*maximum value for exp field is 254*/
    /*max exp is 254-127 = 127*/
    /*min val for exp field is 1
     * so the miv val for exp is 1-127 = -126*/

    /*in denormalized, exp always 0
     * powers of two represnted by frac field
     * 2^-150 is lowest, 2^-127 is max*/
        if (x<-150){
            return 0;
        }

        //DENORMALIZED CASE
        //left shift -> 2^#of bits shifted
        if (x >= -150 && x <= -127){
            int toShift = 0x01;
            toShift = toShift << (-x-bias);
            return toShift;
        }


        //RESULTS IN ALL 1's
        if (x>=128){
            int inf = 0xFF<<23;
            return inf;
        }
        //NORMALIZED
        if (x >=-126 && x <= 127){
            int norm = (x + bias) << 23;
            return norm;
        }
    return 0; 
}
