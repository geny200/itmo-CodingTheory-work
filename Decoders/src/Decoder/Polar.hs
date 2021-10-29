module Decoder.Polar (oddTrim, s, evenTrim, decode, sgn) where

import Chanel.BEC.Probabilities (frozenBits, toProbability)

decodeBit :: (Ord a, Num a) => a -> Bool
decodeBit v
  | v <= 0 = True
  | otherwise = False

oddTrim :: [a] -> [a]
oddTrim [] = []
oddTrim (x : _ : xs) = x : oddTrim xs
oddTrim (x : _) = [x]

evenTrim :: [a] -> [a]
evenTrim [] = []
evenTrim (_ : x : xs) = x : evenTrim xs
evenTrim (_ : x) = x

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
      a = s u divI (oddTrim word)
      b = s u divI (evenTrim word)
   in if modI == 0
        then sgn a * sgn b * min (abs a) (abs b)
        else
          if u !! (length u - (i -1) - 1)
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
        currentBit = decodeBit (s previous n word)
     in currentBit : previous

decode :: (Ord a, Num a) => Int -> Int -> [a] -> [Int]
decode n k word =
  let frozen = reverse (frozenBits (toProbability (0.5 :: Double)) n k)
   in map fromEnum (reverse (decodeStep (length word - 1) word frozen))
