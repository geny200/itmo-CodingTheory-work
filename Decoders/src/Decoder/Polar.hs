module Decoder.Polar (evenTrim, s, oddTrim, decode, sgn) where

import Chanel.BEC.Probabilities (frozenBits, toProbability)

decodeBit :: (Ord a, Num a) => a -> Bool
decodeBit v
  | v <= 0 = True
  | otherwise = False

evenTrim :: [a] -> [a]
evenTrim [] = []
evenTrim (x : _ : xs) = x : evenTrim xs
evenTrim (x : _) = [x]

oddTrim :: [a] -> [a]
oddTrim [] = []
oddTrim (_ : x : xs) = x : oddTrim xs
oddTrim (_ : x) = x

xor' :: Bool -> Bool -> Bool
xor' True False = True
xor' False True = True
xor' _ _ = False

xorV :: [Bool] -> [Bool] -> [Bool]
xorV (x : xs) (y : ys) = (x `xor'` y) : xorV xs ys
xorV _ _ = []

sgn :: (Num a, Ord a) => a -> a
sgn x
  | x < 0 = -1
  | otherwise = 1

s ::
  (Ord a, Num a) =>
  [Bool] -> -- Previous bits
  Int -> -- i
  [a] -> -- word
  a
s _ _ [x] = x
s u i word =
  let (divI, modI) = i `quotRem` 2
      a = s (evenTrim u `xorV` oddTrim u) divI (evenTrim word)
      b = s (oddTrim u) divI (oddTrim word)
   in if modI == 0
        then sgn a * sgn b * min (abs a) (abs b)
        else
          if u !! (i - 1)
            then - a + b
            else a + b

checkHead :: (Ord a) => a -> [a] -> Bool
checkHead _ [] = False
checkHead y (x : _) = y == x

decodeStep :: (Ord a, Num a) => Int -> [a] -> [Int] -> [Bool]
decodeStep (-1) _ _ = []
decodeStep n word frozen
  | n < 0 = []
  | checkHead n frozen =
    let previous = decodeStep (n - 1) word (tail frozen)
     in False : previous
  | otherwise =
    let previous = decodeStep (n - 1) word frozen
        currentBit = decodeBit (s (reverse previous) n word)
     in currentBit : previous

decode :: (Ord a, Num a) => Int -> Int -> [a] -> [Int]
decode n k word =
  let frozen = reverse (frozenBits (toProbability (0.5 :: Double)) n k)
   in map fromEnum (reverse (decodeStep (length word - 1) word frozen))
