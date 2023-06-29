#!/usr/bin/env sh


set -e

build_symk() {
  echo "Building symk..."
  cd server/third_party/symk &&\
  ./build.py &&\
  cd ../../..
}

main() {
  build_symk
}

echo "Start building"
main